from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("vendors/", views.VendorListView.as_view(), name='vendors'),
    path('vendor-detail/<str:pk>', views.VendorDetailView.as_view(), name='vendor-detail'),
    path('items/',views.ItemListView, name='items'),
    path('item-detail/<str:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('purchaseorders/', views.PurchaseOrderListView, name='purchaseorders'),
    path('purchaseorder-detail/<str:pk>', views.PurchaseOrderDetailView, name='purchaseorder-detail'),
    path('invoices/', views.SalesInvoiceListView, name='invoices'),
    path('invoice-detail/<str:pk>', views.SalesInvoiceDetailView, name='invoice-detail'),
    path('approvals/', views.ApprovalListView, name='approvals'),
]