from django.urls import path

from myimpact import views


urlpatterns = [
        path('', views.get_address, name='get_address'),
        path('address_list/', views.address_list, name='address_list'),
        path('address_search/', views.address_search, name='address_search'),
    ]
