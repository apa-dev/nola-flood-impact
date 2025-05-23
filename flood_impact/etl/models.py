import os
import re
import zipfile

import geopandas as gpd
import pandas as pd
from shapely import wkt
import numpy as np

import requests
from django.conf import settings
from django.contrib.gis.db import models
from django.db.models import JSONField
from django.utils import timezone

from etl.data_config import socrata as socrata_config


class SocrataCatalogItem(models.Model):
    """An individual record from the catalog of available datasets
    available on any Socrata-powered data portal accessible at
    <opendata-domain>/data.json.
    """

    access_level = models.CharField(max_length=255, null=True, blank=True)
    contact_point = JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    distribution = JSONField(null=True, blank=True)
    identifier = models.CharField(max_length=255, unique=True)
    issued = models.DateField(null=True, blank=True)
    landing_page = models.URLField(max_length=255, null=True, blank=True)
    modified = models.DateField(null=True, blank=True)
    publisher = JSONField(null=True, blank=True)
    orig_file_loc = models.CharField(max_length=255, null=True, blank=True)
    last_downloaded_on = models.DateTimeField(null=True, blank=True)

    # TODO: full-text search
    title = models.CharField(max_length=255)

    # TODO: assumes format= querystring parameter is always at the end,
    # should make it more robust.
    DISTRIBUTION_FORMAT_PATTERN = re.compile('format=(\w+$)')

    def __repr__(self):
        return '<SocrataCatalogItem: {}>'.format(self.title)

    def get_distribution_type_url(self, type_):
        """Get the download URL for a "distribution" for datasets
        that are not easily served up as JSON over a REST API. Typically,
        these are large files (such as geospatial files) or files in
        proprietary formats (such as Microsoft Excel or Access)

        Args:
            type_ (str): A string representation of the type of
            distribution to download. TODO: standardize this, but
            for now, use :meth:`get_distribution_types` for available formats

        Returns:
            tuple: (str: URL, str: file extension)
        """
        if not self.distribution:
            return (None, None)
        pattern = re.compile('format={}$'.format(type_))
        for dist in self.distribution:
            downloadURL = dist.get('downloadURL', '')
            search = pattern.search(dist.get('downloadURL', ''),
                                    re.IGNORECASE)
            if search is not None:
                return search.string, socrata_config.MIME_EXTENSIONS.get(dist['mediaType'], '')
            return downloadURL, socrata_config.MIME_EXTENSIONS.get(dist['mediaType'], '')

    def get_distribution_types(self):
        """Get all the format=<type> values for the distribution.

        Returns:
            list
        """
        types = []
        for dist in self.distribution:
            search = self.DISTRIBUTION_FORMAT_PATTERN.search(
                    dist.get('downloadURL', ''),
                    re.IGNORECASE)
            if search is not None:
                types.append(search.group(1))
        return types

    @property
    def slug(self):
        """Get the slug that uniquely identifies this dataset across
        all Socrata open data portals.

        Returns:
            str
        """
        return self.identifier.split('/')[-1]

    @property
    def orig_dir(self):
        """Get the default original directory, based on the values in data_config.socrata

        Returns:
            str
        """
        return os.path.join(socrata_config.DATASTORE,
                            socrata_config.DATASTORE_ORIG_NAME)

    @property
    def staging_dir(self):
        """Get the default staging directory, based on the values in data_config.socrata

        Returns:
            str
        """
        return os.path.join(socrata_config.DATASTORE,
                            socrata_config.DATASTORE_STAGING_NAME,
                            'sci_{}'.format(self.pk))

    def get_staging_file_list(self):
        """Get the list of files in this item's staging directory

        Returns:
            list
        """
        if os.path.exists(self.staging_dir):
            return os.listdir(self.staging_dir)
        return []

    def get_staged_file_path(self, name=None, extension=None):
        """Get the full path to a file in the staging directory,
        either by its exact name (with extension) or by only its extension.
        Note that if you select the extension method, this function will return
        the first file that matches.

        Args:
            name (str): Optional, the exact filename (with extension)
            extension (str): Optional, the file extension
        Returns:
            str
        """
        if name is not None:
            return os.path.join(self.staging_dir, name)
        if extension is not None:
            matches = [i for i in self.get_staging_file_list() if i.endswith(extension)]
            if matches:
                return os.path.join(self.staging_dir, matches[0])

    def download_distribution(self, url, extension, datastore=socrata_config.DATASTORE):
        """Download a file pointed to by one of the distribution URLs

        Args:
            url (str): The URL to fetch
            extension (str): The file extension to use for the downloaded file
            datastore (str): Path to a directory to store the downloaded files
        Returns:
            None
        """
        # TODO: Would be nice to have semantically meaningful filenames, instead of
        # sci_<pk>
        fname = 'sci_{}.{}'.format(self.pk, extension)
        if not os.path.exists(self.orig_dir):
            os.makedirs(self.orig_dir)
        path = os.path.join(self.orig_dir, fname)
        req = requests.get(url=url,
                           stream=True,
                           headers={'X-App-Token': settings.SOCRATA_APP_TOKEN}
                           )
        req.raise_for_status()
        with open(path, 'wb') as outfile:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    outfile.write(chunk)
        self.orig_file_loc = path
        self.last_downloaded_on = timezone.now()
        self.save()

    def extract_zip(self, path, extract_dir=None):
        """Extract a zip file

        Args:
            path (str): The path to the zipfile to extract
            extract_dir (str): Optional directory to extract the files to.
                               If left blank, will default to the value configured
                               in data_config.socrata (imported in this module as
                               socrata_config)
        Returns:
            list: The list of paths to the extracted files
        NOTE:
        nola.gov data used to be offered in shapefile format, hence the need to extract files from a zip
        this is no longer the case; it is now offered in csv, rdf, json or xml formats
        """
        if extract_dir is None:
            extract_dir = os.path.join(socrata_config.DATASTORE,
                                       socrata_config.DATASTORE_STAGING_NAME,
                                       'sci_{}'.format(self.pk))
            if not os.path.exists(extract_dir):
                os.makedirs(extract_dir)
        try:
            zf = zipfile.ZipFile(path)
            zf.extractall(path=extract_dir)
            return [os.path.join(extract_dir, x) for x in zf.namelist()]
        except Exception as exc:
            # if extract fails, Convert the CSV to a Shapefile and save it in staging
            csvfile = path
            shapefile = extract_dir + '/sci_{}'.format(self.pk) + '.shp'
            self.csv_to_shp(csvfile, shapefile)
            shp_file_paths = [os.path.join(extract_dir, x) for x in os.listdir(extract_dir)
                  if os.path.isfile(os.path.join(extract_dir, x)) and x.endswith('.shp')]
            return shp_file_paths

    def csv_to_shp(self, csv_file, shapefile_path):
        df = pd.read_csv(csv_file)
        # MUST REFER TO FULL FIELD NAMES HERE (FROM THE CSV):
        string_columns = ['Site Address ID', 'Full Address Number', 'Address Number Prefix', 'Address Number Suffix', 
            'Zoning Number', 'Zoning Year']
        for col in string_columns:
            if col in df.columns:
                df[col] = df[col].astype(str)
        # if path is parcels (sci_188) then we need to convert geopin to string
        if shapefile_path.find('sci_188') >= 0:
            string_columns = ['GEOPIN',]
            for col in string_columns:
                if col in df.columns:
                    df[col] = df[col].astype(str)

        # Check if LAT and LONG columns are present
        if 'LAT' in df.columns and 'LONG' in df.columns:
            df_clean = df.dropna(subset=['LAT', 'LONG'])
            df_clean = df_clean[np.isfinite(df_clean['LAT']) & np.isfinite(df_clean['LONG'])]
            gdf = gpd.GeoDataFrame(df_clean, geometry=gpd.GeoSeries.from_wkt(df['the_geom']))
            gdf.set_crs("EPSG:4326", inplace=True)

        elif 'the_geom' in df.columns:
            df_clean = df[df['the_geom'].apply(lambda x: isinstance(x, str))]
            geometry = df_clean['the_geom'].apply(wkt.loads)
            gdf = gpd.GeoDataFrame(df_clean, geometry=geometry)
            gdf = gdf.dropna(subset=['geometry',])

            if shapefile_path.find('sci_148') >= 0 or shapefile_path.find('sci_188') >= 0:
                gdf = gdf.dropna(subset=['GEOPIN',])

            gdf.set_crs("EPSG:4326", inplace=True)

        else:
            raise ValueError("CSV file does not contain 'LAT'/'LONG' columns or a recognized geometry field (e.g., 'the_geom').")

        gdf.to_file(shapefile_path)
        print(f"Shapefile saved to: {shapefile_path}")
