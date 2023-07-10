from django.urls import path 
from . import views
from inventory.views import VendorListView

urlpatterns = [
    path("", views.index, name='index'),
    path("vendor", VendorListView.as_view(), name='vendor'),
    path('purchaseorder',views.purchaseorder, name='purchaseorder'),
    path('salesinvoice', views.salesinvoice, name='salesinvoice'),
]