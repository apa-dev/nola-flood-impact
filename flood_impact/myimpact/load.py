from django.contrib.gis.utils import LayerMapping

from etl.models import SocrataCatalogItem
from myimpact.models import BuildingFootprint, Parcel, SiteAddressPoint, ZoningDistrict


def parcels():
    parcels = SocrataCatalogItem.objects.get(title='Parcels')
    url, extension = parcels.get_distribution_type_url('Shapefile')
    parcels.download_distribution(url, extension)
    parcels.extract_zip(parcels.orig_file_loc)
    parcels_shp = parcels.get_staged_file_path(extension='shp')

    parcels_mapping = {
            'object_id': 'objectid',
            'shape_area': 'shape_area',
            'hectares': 'hectares',
            'acres': 'acres',
            'perimeter': 'perimeter',
            'geopin': 'geopin',
            'shape_length': 'shape_leng',
            'the_geom': 'MULTIPOLYGON'
        }
    lm = LayerMapping(
            Parcel, parcels_shp, parcels_mapping, transform=False, encoding='iso-8859-1'
            )

    lm.save(strict=True, verbose=True)


def building_footprints():
    fps = SocrataCatalogItem.objects.get(title='Building Footprint')
    # url, extension = fps.get_distribution_type_url('Shapefile')
    # fps.download_distribution(url, extension)
    # fps.extract_zip(fps.orig_file_loc)
    fps_shp = fps.get_staged_file_path(extension='shp')

    fps_mapping = {
        'num_stories': 'numstories',
        'shape_length': 'shape_leng',
        'shape_area': 'shape_area',
        'feature_code': 'featurecod',
        'geopin': 'geopin',
        'object_id': 'objectid',
        'building_height': 'bldgheight',
        'the_geom': 'MULTIPOLYGON'
        }
    lm = LayerMapping(
            BuildingFootprint, fps_shp, fps_mapping, transform=False, encoding='iso-8859-1'
            )
    lm.save(strict=True, verbose=True)


def zoning_districts():
    zds = SocrataCatalogItem.objects.get(title='Zoning District')
    # url, extension = zds.get_distribution_type_url('Shapefile')
    # zds.download_distribution(url, extension)
    # zds.extract_zip(zds.orig_file_loc)
    zds_shp = zds.get_staged_file_path(extension='shp')

    zds_mapping = {
            'zone_number': 'zonenum',
            'created_by': 'created_us',
            'zone_description': 'zonedesc',
            'object_id': 'objectid',
            'zone_year': 'zoneyear',
            'future_land_use': 'futlanduse',
            'ordinance_number': 'ordnum',
            'zone_class': 'zoneclass',
            'last_edited_by': 'last_edite',
            'flu_link': 'flu_link',
            'flu_description': 'flu_desc',
            'date_last_edited': 'date_last_',
            'time_last_edited': 'time_last_',
            'hyperlink': 'hyperlink',
            'date_created': 'date_creat',
            'time_created': 'time_creat',
            'the_geom': 'MULTIPOLYGON'
        }

    lm = LayerMapping(ZoningDistrict, zds_shp, zds_mapping, transform=False,
                      encoding='iso-8859-1')
    # Some features have null geometries, so we set strict=False (i.e., ignore it, don't import)
    lm.save(strict=False, verbose=True)


def site_address_points():
    site_address_point_mapping = {
            'address_type': 'addr_type',
            'alt_unit_id': 'altunitid',
            'source': 'source',
            'address_number': 'addrnum',
            'easting': 'long',
            'full_name': 'fullname',
            'address_number_suffix': 'addrnumsuf',
            'object_id': 'objectid',
            'pre_address_number': 'preaddrnum',
            'alt_unit_type': 'altunittyp',
            'capture_method': 'capturemet',
            'address_range': 'addrrange',
            'address_point_key': 'addptkey',
            'status': 'status',
            'point_type': 'pointtype',
            'full_address': 'fulladdr',
            'northing': 'lat',
            'place_name': 'placename',
            'unit_type': 'unittype',
            'municipality': 'municipali',
            'site_address_id': 'siteaddid',
            'last_editor': 'lasteditor',
            'date_last_updated': 'date_lastu',
            'time_last_updated': 'time_lastu',
            'the_geom': 'POINT'
            }

    site_address_points = SocrataCatalogItem.objects.get(title='Site Address Point')
    site_address_points_shp = site_address_points.get_staged_file_path(extension='shp')

    lm = LayerMapping(
            SiteAddressPoint, site_address_points_shp, site_address_point_mapping,
            transform=False, encoding='iso-8859-1',
            )
    lm.save(strict=True, verbose=True)
