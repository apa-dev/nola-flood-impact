import os
import re
from pathlib import Path

from django.test import TestCase

from etl.data_config import socrata
from etl.models import SocrataCatalogItem


class SocrataCatalogItemTestCase(TestCase):

    # Parcels
    IDENTIFIER = 'https://data.nola.gov/api/views/4tiv-n7fd'

    def setUp(self):
        distribution = [
            {'@type': 'dcat:Distribution',
                'mediaType': 'application/vnd.google-earth.kml+xml',
                'downloadURL': 'https://data.nola.gov/api/geospatial/4tiv-n7fd?method=export&format=KML'},
            {'@type': 'dcat:Distribution',
                'mediaType': 'application/vnd.google-earth.kmz',
                'downloadURL': 'https://data.nola.gov/api/geospatial/4tiv-n7fd?method=export&format=KMZ'},
            {'@type': 'dcat:Distribution',
                'mediaType': 'application/zip',
                'downloadURL': 'https://data.nola.gov/api/geospatial/4tiv-n7fd?method=export&format=Shapefile'},
            {'@type': 'dcat:Distribution',
                'mediaType': 'application/zip',
                'downloadURL': 'https://data.nola.gov/api/geospatial/4tiv-n7fd?method=export&format=Original'},
            {'@type': 'dcat:Distribution',
                'mediaType': 'application/json',
                'downloadURL': 'https://data.nola.gov/api/views/y8at-d22k/rows.json?accessType=DOWNLOAD'},
            {'@type': 'dcat:Distribution',
                'mediaType': 'text/csv',
                'downloadURL': 'https://data.nola.gov/api/views/y8at-d22k/rows.csv?accessType=DOWNLOAD'},
            {'@type': 'dcat:Distribution',
                'mediaType': 'application/zip',
                'downloadURL': 'https://data.nola.gov/api/geospatial/4tiv-n7fd?method=format&format=Geopkg'},
            {'@type': 'dcat:Distribution',
                'mediaType': 'application/zip',
                'downloadURL': 'https://data.nola.gov/api/geospatial/4tiv-n7fd?export=GeoJSON&format=GDB'}
        ]

        self.catalog_item = SocrataCatalogItem.objects.create(
                distribution=distribution,
                identifier=self.IDENTIFIER,
                title='Parcels'
            )

    def test_get_distribution_types(self):
        dist_types = self.catalog_item.get_distribution_types()

        self.assertIn('KMZ', dist_types)
        self.assertIn('KML', dist_types)
        self.assertIn('Shapefile', dist_types)
        self.assertIn('Original', dist_types)
        self.assertIn('Geopkg', dist_types)
        self.assertIn('GDB', dist_types)
        self.assertNotIn('GeoJSON', dist_types)
        self.assertNotIn('format', dist_types)
        self.assertNotIn('export', dist_types)

    def test_get_distribution_type_url(self):
        catalog_item = SocrataCatalogItem.objects.get(identifier=self.IDENTIFIER)
        shapefile_url = catalog_item.get_distribution_type_url('Shapefile')
        self.assertEqual(
                shapefile_url[0],
                'https://data.nola.gov/api/geospatial/4tiv-n7fd?method=export&format=Shapefile'
                )
        self.assertEqual(
                shapefile_url[1],
                'zip'
                )
        self.assertNotEqual(
                shapefile_url[0],
                'https://data.nola.gov/api/geospatial/4tiv-n7fd?method=export&format=KML'
                )
        self.assertIsNone(catalog_item.get_distribution_type_url('GeoJSON'))

    def test_slug(self):
        slug_pattern = re.compile('\w{4}-\w{4}', re.ASCII)
        catalog_item = SocrataCatalogItem.objects.get(identifier=self.IDENTIFIER)

        self.assertIsNotNone(slug_pattern.search(catalog_item.slug))

    def test_datastore_location_is_accessible(self):
        fname = os.path.join(socrata.DATASTORE, 'test')
        Path(fname).touch()
        self.assertIsNotNone(os.stat(fname))
        os.unlink(fname)
