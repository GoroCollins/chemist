from django.urls import path 
from allauth.account.views import SignupView
from . import views

app_name = "inventory"

urlpatterns = [
    path("", SignupView.as_view(), name='index'),
    path("home/", views.index, name='home'),
    path("units/", views.UnitListView.as_view(), name='units'),
    path("unit-detail/<str:pk>/", views.UnitDetailView.as_view(), name='unit-detail'),
    path("unit/add/", views.UnitCreateView.as_view(), name='unit-add'),
    path("unit/<str:pk>/", views.UnitUpdateView.as_view(), name="unit-update"),
    path("vendors/", views.VendorListView.as_view(), name='vendors'),
    path('vendor-detail/<str:pk>/', views.VendorDetailView.as_view(), name='vendor-detail'),
    path("vendor/add/", views.VendorCreateView.as_view(), name="vendor-add"),
    path("vendor/<str:pk>/", views.VendorUpdateView.as_view(), name="vendor-update"),
    path('items/',views.ItemListView.as_view(), name='items'),
    path('item-detail/<str:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path("item/add/", views.ItemCreateView.as_view(), name="item-add"),
    path("item/<str:pk>/", views.ItemUpdateView.as_view(), name="item-update"),
    path('purchaseorders/', views.PurchaseHeaderListView.as_view(), name='purchaseorders'),
    path('purchaseorder-detail/<str:pk>/', views.PurchaseHeaderDetailView.as_view(), name='purchaseorder-detail'),
    path("purchaseorder/add/", views.PurchaseOrderCreate.as_view(), name="purchaseorder-create"),
    path("purchase/<str:pk>/",views.PurchaseOrderUpdate.as_view(), name="purchaseorder-update"),
    path('purchasememos/', views.PurchaseCreditMemoListView.as_view(), name='purchasememos'),
    path('purchasememo-detail/<str:pk>', views.PurchaseCreditMemoDetailView.as_view(), name='purchasememo-detail'),
    path("purchasememos/add/", views.PurchaseCreditMemoCreate.as_view(), name='purchasememo-create'),
    path('invoices/', views.SalesInvoiceListView.as_view(), name='invoices'),
    path('invoice-detail/<str:pk>/', views.SalesInvoiceDetailView.as_view(), name='invoice-detail'),
    path("invoice/add/", views.SalesInvoiceCreate.as_view(), name='invoice-create'),
    path("invoice/<str:pk>/",views.SalesInvoiceUpdate.as_view(), name="invoice-update"),
    path('salesmemos/', views.SalesCreditMemoListView.as_view(), name='salesmemos'),
    path('salesmemo-detail/<str:pk>', views.SalesCreditMemoDetailView.as_view(), name='salesmemo-detail'),
    path("salesmemo/add/", views.SalesCreditMemoCreate.as_view(), name="salesmemo-create"),
    path('approvals/', views.ApprovalListView.as_view(), name='approvals'),
    path('approval-detail/<int:pk>/', views.ApprovalDetailView.as_view(), name='approval-detail'),
    path('approval/<str:pk>/', views.ApprovalUpdateView.as_view(), name="approval-update"),
    path('create-approval/', views.create_approval_request, name="create-approval"),
    path('profile/', views.UserProfile.as_view(), name='user-profile' ),
    path('invoice-printout/<str:pk>/', views.sales_pdf, name='invoiceprintout'),
    path('lpo-printout/<str:pk>/', views.purchases_pdf, name='lpoprintout'),
]

