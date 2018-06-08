from django.urls import include, path
from rest_framework import routers

from myimpact import views


router = routers.DefaultRouter()
# router.register(r'site_address_point', views.SiteAddressPointViewset)


urlpatterns = [
        path('', views.index, name='index'),
        path('address_list/', views.address_list, name='address_list'),
        path('address_search/', views.address_search, name='address_search'),
        path('address/<str:address>/', views.address_detail, name='address_detail'),
        # path('site_address_point/', include(router.urls)),
    ]
