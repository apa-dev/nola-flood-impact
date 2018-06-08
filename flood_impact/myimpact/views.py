import json
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from myimpact.forms import AddressForm
from myimpact.models import SiteAddressPoint
from myimpact.serializers import SiteAddressPointSerializer


class MyImpactResponse(TemplateView):
        pass


def index(request):
    return render(request, 'myimpact/index.html')


def address_list(request):
    """
    Return all unique addresses in the SiteAddressPoint model
    """

    # This list of distinct addresses won't change until we re-import an updated
    # SiteAddressPoint shapefile, so for now just load a
    # JSON file of them to get around this very non-performant query
    # addresses = list(SiteAddressPoint.objects.values_list('full_address', flat=True)
    #                                          .distinct('full_address'))
    addresses = json.load(open(
        os.path.join(settings.BASE_DIR, 'myimpact/static/myimpact/addresses.json')
        ))
    return JsonResponse(addresses, safe=False)


# DJANGO...Y U NO SET COOKIE?
@csrf_exempt
def address_search(request):
    """Search for an address"""

    if request.method == "POST" and request.content_type == "application/json":

        if request.body:
            data = json.loads(request.body)
            query = data.get('query', '')

            results = SiteAddressPoint.objects.filter(full_address__search=query)\
                                              .values_list('full_address', flat=True)\
                                              .order_by('full_address')
            return JsonResponse(list(results), safe=False)


def address_detail(request, address):
    """Display the address detail view"""
    # address = get_object_or_404(SiteAddressPoint, full_address=address)
    address = SiteAddressPoint.objects.filter(full_address=address)
    # TODO: Dedupe
    if address.count() >= 1:
        return JsonResponse(address.first().json_response())
    return JsonResponse({'success': False,
                         'message': 'Could not get an exact match for {}'.format(address)
                         })


# class SiteAddressPointViewset(viewsets.ModelViewSet):
#     queryset = SiteAddressPoint.objects.all()
#     serializer_class = SiteAddressPointSerializer
