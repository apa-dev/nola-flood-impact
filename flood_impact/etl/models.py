import os
import re
import requests

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField

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
            tuple: (str: URL, str: mediaType)
        """

        if not self.distribution:
            return
        pattern = re.compile('format={}$'.format(type_))
        for dist in self.distribution:
            search = pattern.search(dist.get('downloadURL', ''),
                                    re.IGNORECASE)
            if search is not None:
                return search.string, socrata_config.MIME_EXTENSIONS.get(dist['mediaType'], '')

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

    def download_distribution(self, url, extension, datastore=socrata_config.DATASTORE):
        """Download a file pointed to by one of the distribution URLs

        Args:
            url (str): The URL to fetch
            extension (str): The file extension to use
            datastore (str): File path to a directory to store the downloaded files
        Returns:
            str: The full path to the downloaded file
        """
        # TODO: Would be nice to have semantically meaningful filenames, instead of
        # sci_id
        fname = 'sci_{}.{}'.format(self.pk, extension)
        path = os.path.join(datastore, 'orig', fname)
        req = requests.get(url=url,
                           stream=True,
                           headers={'X-App-Token': settings.SOCRATA_APP_TOKEN}
                           )
        with open(path, 'wb') as outfile:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    outfile.write(chunk)
        return path
