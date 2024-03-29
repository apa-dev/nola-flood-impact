# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.db.models import Union
from django.contrib.auth.models import AbstractUser

from myimpact.calculator import FloodImpactCalculator


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

    def __repr__(self):
        return '<SiteAddressPoint: {}>'.format(self.full_address)

    def get_containing_parcel(self):
        """Get the Parcel that contains this address point

        Returns:
            Parcel
        """
        parcel = Parcel.objects.filter(the_geom__contains=self.the_geom)
        if parcel.count() == 1:
            return parcel.first()

    def get_building(self):
        """Get the BuildingFootprint that contains (or is closest to the containing
        parcel of) this address point

        Returns:
            BuildingFootprint
        """
        building = BuildingFootprint.objects.filter(the_geom__contains=self.the_geom)
        if building.count() == 1:
            return building.first()
        elif building.count() == 0:
            # Address points are not always placed on the building
            # get the containing parcel
            parcel = self.get_containing_parcel()
            if parcel is not None:
                # get the buildings
                buildings = parcel.get_buildings()
                if buildings.count() == 1:
                    return buildings.first()
                elif buildings.count() > 1:
                    # return the building that has the most overlapping area
                    intersecting_areas = []
                    for building in buildings:
                        intersecting_areas.append(
                                (building.pk,
                                 building.the_geom.transform(
                                     settings.LOUISIANA_SOUTH_EPSG, clone=True)
                                 .intersection(parcel.the_geom.transform(
                                         settings.LOUISIANA_SOUTH_EPSG, clone=True)).area)
                            )
                    pk = sorted(intersecting_areas,
                                key=lambda x: x[1],
                                reverse=True)[0][0]
                    return BuildingFootprint.objects.get(pk=pk)

    def get_zoning(self):
        """Get the zoning district that contains this address point

        Returns:
            ZoningDistrict
        """
        zoning_district = ZoningDistrict.objects.filter(the_geom__contains=self.the_geom)
        if zoning_district.count() == 1:
            return zoning_district.first()

    def get_cover_type(self, default="URBAN_RES"):
        """Get the pervious surface coverage type (defined in myimpact.calculator)
        for this address, based on the NOLA_ZONING_COVER_TYPE_MAPPING, also defined
        in myimpact.calculator.

        Args:
            default (str): The default cover type to use if we missed one in the
                           mapping, or if we have issues with whatever janky character
                           encoding the zoning shapefile is in that's causing é to
                           render as ?. I've tried iso-8859-1, latin1, utf-8, and...welp
        Returns:
            tuple
        """
        zoning = self.get_zoning()
        if zoning is None:
            zoning_cover_type = default
        else:
            description = zoning.zone_description
            zoning_cover_type = settings.NOLA_ZONING_COVER_TYPE_MAPPING.get(
                    description, default
                    )
        return next(x for x in settings.COVER_TYPES if x[0] == zoning_cover_type)

    def create_flood_calculator(self, area_breakdown, rainfall=1.5):
        """Instantiate FloodImpactCalculator objects, based on the
        area_breakdown (return value of Parcel.area_breakdown).
        Non-building area will get the cover_type that maps to its zoning designation
        Building area will be presumed to be impervious (cover_type = IMPERVIOUS)

        Args:
            area_breakdown (dict): return value of Parcel.area_breakdown
        Returns:
            dict, of myimpact.FloodImpactCalculator, keyed by [non]building area
        """
        cover_type = self.get_cover_type()
        non_building_area = area_breakdown['totals']['non_building']
        building_area = area_breakdown['totals']['building']
        calc_non_building_area = FloodImpactCalculator(cover_type=cover_type[0],
                                                       area_square_feet=non_building_area,
                                                       rainfall=rainfall)
        calc_building_area = FloodImpactCalculator(cover_type="IMPERVIOUS",
                                                   area_square_feet=building_area,
                                                   rainfall=rainfall)
        return {
                'building': calc_building_area,
                'non_building': calc_non_building_area
                }

    def json_response(self, rainfall=1.5):
        cover_type = self.get_cover_type()
        parcel = self.get_containing_parcel()
        zone_description = 'Unknown'
        zoning = self.get_zoning()
        if zoning is not None:
            zone_description = zoning.zone_description
        if parcel is not None:
            calculator = self.create_flood_calculator(parcel.area_breakdown, rainfall)
            cnb = calculator['non_building']
            cb = calculator['building']
            return {
                    'success': True,
                    'result': {
                        'address': self.full_address,
                        'parcel_geopin': parcel.geopin,
                        'zoning_description': zone_description,
                        'non_building_area': round(cnb.area_square_feet, 1),
                        'building_area': round(cb.area_square_feet, 1),
                        'non_building_cover_type': cover_type[1],
                        'non_building_runoff_curve_number': cnb.runoff_curve_number,
                        'non_building_soil_retention': round(cnb.soil_retention, 1),
                        'non_building_runoff_volume': round(cnb.calc_runoff_volume(), 1),
                        'building_runoff_volume': round(cb.calc_runoff_volume(), 1),
                        'total_runoff_volume': round(cnb.calc_runoff_volume() +
                                                     cb.calc_runoff_volume(), 1),
                        "geojson": parcel.geojson_response(),
                        "center": parcel.centroid
                        }
                    }
        return {
                'success': False,
                'message': 'Unable to locate parcel from this address'
                }


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

    def __repr__(self):
        return '<Parcel: {}>'.format(self.geopin)

    def get_buildings(self):
        """Get all the BuildingFootprint intersecting this Parcel

        Returns:
            django.db.models.query.QuerySet
        """
        return BuildingFootprint.objects.filter(the_geom__intersects=self.the_geom)

    def get_building_intersection(self):
        """Get the intersection of this parcel's geometry and the unioned geometry of all buildings intersecting
        this parcel

        Returns:
            django.contrib.gis.geos.collections.MultiPolygon
        """
        buildings = self.get_buildings()
        if buildings.count() > 0:
            # Union the geometry of all buildings intersecting the parcel
            unioned_buildings = buildings.aggregate(unioned=Union('the_geom'))['unioned']
            # Take the intersection of the parcel and the unioned building geometry
            return unioned_buildings.intersection(self.the_geom)

    def get_non_building_geometry(self):
        """Get the geometry of the parcel with all building footprint geometry removed

        Returns:
            django.contrib.gis.geos.collections.MultiPolygon
        """
        building_intersection = self.get_building_intersection()
        if building_intersection is not None:
            return self.the_geom.difference(building_intersection)

    @property
    def centroid(self):
        return list(self.the_geom.centroid)

    @property
    def geom_geojson(self):
        """Return the Parcel geometry as GeoJSON"""
        return json.loads(self.the_geom.json)

    @property
    def building_intersection_geojson(self):
        """Get the total building geometry intersection on this Parcel"""
        buildings = self.get_building_intersection()
        if buildings:
            return json.loads(buildings.json)

    @property
    def non_building_geometry_geojson(self):
        """Get the non-building geometry as GeoJSON"""
        nbg = self.get_non_building_geometry()
        if nbg:
            return json.loads(nbg.json)

    def geojson_response(self):
        """Create individual GeoJSON objects of the parcel itself and [non]building geometry"""
        resp = {
                "parcel": {
                    "type": "Feature",
                    "id": self.pk,
                    "properties": {
                        "area": self.area_breakdown,
                        "geopin": self.geopin
                        },
                    "geometry": self.geom_geojson
                    },
                "building": {
                    "type": "Feature",
                    "properties": {},
                    "geometry": self.building_intersection_geojson or {}
                    },
                "nonbuilding": {
                    "type": "Feature",
                    "properties": {},
                    "geometry": self.non_building_geometry_geojson or {}
                    }
                }
        return resp

    @property
    def area_breakdown(self):
        """Get the non-building area of this parcel in square feet

        Returns:
            dict
        """
        non_building_geom = self.get_non_building_geometry()
        if non_building_geom is not None:
            non_building_area = non_building_geom.transform(
                    settings.LOUISIANA_SOUTH_EPSG, clone=True).area
            building_area = self.the_geom.transform(
                    settings.LOUISIANA_SOUTH_EPSG, clone=True).area - non_building_area
            return {
                    "totals": {
                        "non_building": non_building_area,
                        "building": building_area
                        },
                    "units": "square feet"
                    }
        else:
            # No buildings on the parcel, so just use the entire parcel area
            non_building_area = self.the_geom.transform(
                    settings.LOUISIANA_SOUTH_EPSG, clone=True).area
            return {
                    "totals": {
                        "non_building": non_building_area,
                        "building": 0
                        },
                    "units": "square feet"
                    }


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

    def __repr__(self):
        return '<ZoningDistrict: {}>'.format(self.zone_description)
