from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class SiteAddressPoint(models.Model):
    """Model for the "Site Address Point" dataset from NOLA Open Data:
    https://data.nola.gov/d/awd4-9fzf
    """
    address_type = models.CharField(max_length=255, null=True, blank=True)
    alt_unit_id = models.CharField(max_length=255, null=True, blank=True)
    alt_unit_type = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    address_number = models.CharField(max_length=255, null=True, blank=True)
    easting = models.FloatField()
    northing = models.FloatField()
    full_name = models.CharField(max_length=255, null=True, blank=True)
    address_number_suffix = models.CharField(max_length=255, null=True, blank=True)
    object_id = models.FloatField()
    pre_address_number = models.CharField(max_length=255, null=True, blank=True)
    capture_method = models.CharField(max_length=255, null=True, blank=True)
    address_range = models.CharField(max_length=255, null=True, blank=True)
    address_point_key = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    point_type = models.CharField(max_length=255, null=True, blank=True)
    full_address = models.CharField(max_length=255, db_index=True)
    unit_id = models.CharField(max_length=255, null=True, blank=True)
    place_name = models.CharField(max_length=255, null=True, blank=True)
    unit_type = models.CharField(max_length=255, null=True, blank=True)
    municipality = models.CharField(max_length=255, null=True, blank=True)
    site_address_id = models.CharField(max_length=255, null=True, blank=True)
    last_editor = models.CharField(max_length=255, null=True, blank=True)
    date_last_updated = models.DateField(null=True, blank=True)
    time_last_updated = models.CharField(max_length=255, null=True, blank=True)
    the_geom = models.PointField(srid=4326)


class Parcel(models.Model):
    """Model for the Parcels dataset from NOLA Open Data:
    https://data.nola.gov/d/4tiv-n7fd
    """
    object_id = models.FloatField()
    shape_area = models.FloatField()
    hectares = models.FloatField(null=True, blank=True)
    acres = models.FloatField(null=True, blank=True)
    perimeter = models.FloatField(null=True, blank=True)

    # XXX: This should be unique, but is not in the shapefile
    geopin = models.CharField(max_length=255, db_index=True)

    shape_length = models.FloatField()
    the_geom = models.MultiPolygonField(srid=4326)


class BuildingFootprint(models.Model):
    """Model for the Building Footprint dataset from NOLA Open Data:
    https://data.nola.gov/d/m3gg-u447
    """

    num_stories = models.FloatField(null=True, blank=True)
    shape_length = models.FloatField()
    shape_area = models.FloatField()
    feature_code = models.CharField(max_length=255, null=True, blank=True)
    geopin = models.FloatField()
    object_id = models.FloatField()
    building_height = models.FloatField(null=True, blank=True)
    the_geom = models.MultiPolygonField(srid=4326)


class ZoningDistrict(models.Model):
    """Model for the Zoning District dataset from NOLA Open Data:
    https://data.nola.gov/d/25ka-xtj7
    """

    zone_number = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    zone_description = models.CharField(max_length=255, null=True, blank=True)
    object_id = models.FloatField()
    zone_year = models.CharField(max_length=255, null=True, blank=True)
    future_land_use = models.CharField(max_length=255, null=True, blank=True)
    ordinance_number = models.CharField(max_length=255, null=True, blank=True)
    zone_class = models.CharField(max_length=255, null=True, blank=True)
    last_edited_by = models.CharField(max_length=255, null=True, blank=True)
    flu_link = models.CharField(max_length=255, null=True, blank=True)
    flu_description = models.CharField(max_length=255, null=True, blank=True)
    date_last_edited = models.DateField(null=True, blank=True)
    time_last_edited = models.CharField(max_length=255, null=True, blank=True)
    hyperlink = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateField(null=True, blank=True)
    time_created = models.CharField(max_length=255, null=True, blank=True)
    the_geom = models.MultiPolygonField(srid=4326, null=True, blank=True)
