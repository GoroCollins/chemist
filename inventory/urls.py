from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("units/", views.UnitListView.as_view(), name='units'),
    path("unit-detail/<str:pk>/", views.UnitDetailView.as_view(), name='unit-detail'),
    path("unit-create/", views.UnitCreateView.as_view(), name='unit-create'),
    path("vendors/", views.VendorListView.as_view(), name='vendors'),
    path('vendor-detail/<str:pk>/', views.VendorDetailView.as_view(), name='vendor-detail'),
    path('items/',views.ItemListView.as_view(), name='items'),
    path('item-detail/<str:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('purchaseorders/', views.PurchaseHeaderListView.as_view(), name='purchaseorders'),
    path('purchaseorder-detail/<str:pk>/', views.PurchaseHeaderDetailView.as_view(), name='purchaseorder-detail'),
    path('purchasememos/', views.PurchaseCreditMemoListView.as_view(), name='purchasememos'),
    path('purchasememo-detail/<str:pk>', views.PurchaseCreditMemoDetailView.as_view(), name='purchasememo-detail'),
    path('invoices/', views.SalesInvoiceListView.as_view(), name='invoices'),
    path('invoice-detail/<str:pk>/', views.SalesInvoiceDetailView.as_view(), name='invoice-detail'),
    path('salesmemos/', views.SalesCreditMemoListView.as_view(), name='salesmemos'),
    path('salesmemo-detail/<str:pk>', views.SalesCreditMemoDetailView.as_view(), name='salesmemo-detail'),
    path('approvals/', views.ApprovalListView.as_view(), name='approvals'),
    path('approval-detail/<int:pk>/', views.ApprovalDetailView.as_view(), name='approval-detail'),
]