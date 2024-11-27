from django.contrib.gis.utils import LayerMapping

from etl.models import SocrataCatalogItem
from etl.tasks import save_nola_catalog
from myimpact.models import BuildingFootprint, Parcel, SiteAddressPoint, ZoningDistrict


def parcels():
    parcels = SocrataCatalogItem.objects.get(title='Parcels')
    url, extension = parcels.get_distribution_type_url('Shapefile')
    parcels.download_distribution(url, extension)
    parcels.extract_zip(parcels.orig_file_loc)
    parcels_shp = parcels.get_staged_file_path(extension='shp')

    parcels_mapping = {
            'object_id': 'OBJECTID',
            'shape_area': 'Shape.STAr',
            'acres': 'ACRES',
            'perimeter': 'PERIMETER',
            'geopin': 'GEOPIN',
            'shape_length': 'Shape.STLe',
            'the_geom': 'MULTIPOLYGON'
        }
    lm = LayerMapping(
            Parcel, parcels_shp, parcels_mapping, transform=False, encoding='iso-8859-1'
            )

    lm.save(strict=True, verbose=True)


def building_footprints():
    fps = SocrataCatalogItem.objects.get(title='Building Footprint')
    url, extension = fps.get_distribution_type_url('Shapefile')
    fps.download_distribution(url, extension)
    fps.extract_zip(fps.orig_file_loc)
    fps_shp = fps.get_staged_file_path(extension='shp')

    fps_mapping = {
        'shape_length': 'Shape.STLe',
        'shape_area': 'Shape.STAr',
        'geopin': 'GEOPIN',
        'object_id': 'OBJECTID',
        'the_geom': 'MULTIPOLYGON'

        }
    lm = LayerMapping(
            BuildingFootprint, fps_shp, fps_mapping, transform=False, encoding='iso-8859-1'
            )
    lm.save(strict=True, verbose=True)


def zoning_districts():
    zds = SocrataCatalogItem.objects.get(title='Zoning Districts')
    url, extension = zds.get_distribution_type_url('Shapefile')
    zds.download_distribution(url, extension)
    zds.extract_zip(zds.orig_file_loc)
    zds_shp = zds.get_staged_file_path(extension='shp')

    zds_mapping = {
            'zone_number': 'Zoning Num',
            'zone_description': 'Zone Descr',
            'object_id': 'OBJECTID',
            'zone_year': 'Zoning Yea',
            'ordinance_number': 'Zoning Ord',
            'zone_class': 'Zoning Cla',
            'hyperlink': 'HYPERLINK',
            'the_geom': 'MULTIPOLYGON'
        }

    lm = LayerMapping(ZoningDistrict, zds_shp, zds_mapping, transform=False,
                      encoding='iso-8859-1')
    # Some features have null geometries, so we set strict=False (i.e., ignore it, don't import)
    lm.save(strict=False, verbose=True)


def site_address_points():

    site_address_point_mapping = {
            'address_type': 'ADDR_TYPE',
            'source': 'Address So',
            'address_number': 'Full Addre',
            'easting': 'LONG',
            'full_name': 'Full Road',
            'address_number_suffix': 'Address _1',
            'object_id': 'OBJECTID',
            'pre_address_number': 'Address Nu',
            'capture_method': 'Capture Me',
            'status': 'Status',
            'point_type': 'Location',
            'full_address': 'Full Add_1',
            'northing': 'LAT',
            'place_name': 'Place Name',
            'unit_type': 'Address Un',
            'unit_id': 'Address _2',
            'site_address_id': 'Site Addre',
            'last_editor': 'last_edite',
            'time_last_updated': 'last_edi_1',
            'the_geom': 'POINT'
            }

    site_address_points = SocrataCatalogItem.objects.get(title='Site Address Point')
    url, extension = site_address_points.get_distribution_type_url('Shapefile')
    site_address_points.download_distribution(url, extension)
    site_address_points.extract_zip(site_address_points.orig_file_loc)
    site_address_points_shp = site_address_points.get_staged_file_path(extension='shp')

    lm = LayerMapping(
            SiteAddressPoint, site_address_points_shp, site_address_point_mapping,
            transform=False, encoding='iso-8859-1',
            )
    lm.save(strict=True, verbose=True)


def load_all():
    print("Loading addresses, building footprints, parcels, and zoning districts "
          "from https://data.nola.gov. Please be patient, this may take several minutes...")
    save_nola_catalog()
    site_address_points()
    building_footprints()
    parcels()
    zoning_districts()
