from rest_framework_gis.serializers import GeoFeatureModelSerializer

from myimpact.models import SiteAddressPoint


class SiteAddressPointSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = SiteAddressPoint
        geo_field = "the_geom"

        fields = ("full_address",)
