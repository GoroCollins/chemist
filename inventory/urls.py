from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("vendor", views.vendor, name='vendor'),
    path('purchaseorder',views.purchaseorder, name='purchaseorder'),
    path('salesinvoice', views.salesinvoice, name='salesinvoice'),
]