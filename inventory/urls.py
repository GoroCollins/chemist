from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("vendors/", views.VendorListView.as_view(), name='vendors'),
    path('vendor-detail/<str:pk>', views.VendorDetailView.as_view(), name='vendor-detail'),
    path('items/',views.ItemListView.as_view(), name='items'),
    path('item-detail/<str:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('purchaseorders/', views.PurchaseOrderListView.as_view(), name='purchaseorders'),
    path('purchaseorder-detail/<str:pk>', views.PurchaseOrderDetailView.as_view(), name='purchaseorder-detail'),
    path('invoices/', views.SalesInvoiceListView.as_view(), name='invoices'),
    path('invoice-detail/<str:pk>', views.SalesInvoiceDetailView.as_view(), name='invoice-detail'),
    path('approvals/', views.ApprovalListView.as_view(), name='approvals'),
]