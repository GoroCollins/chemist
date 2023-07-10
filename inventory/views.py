from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Item, ItemEntry, PurchaseHeader, PurchaseLine, SalesHeader, SalesLines, Vendor, Unit
# Create your views here.

def index(request):
    # will show items list
    return HttpResponse('List of items')
def item_details(request, item_id):
    try:
        i = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404('Item does not exist')
    return HttpResponse(i)
def vendor(requets):
    # will show vendors list
    return HttpResponse('List of vendors')

def purchaseorder(request):
    # will show purchase orders
    return HttpResponse('List of purchase orders')

def salesinvoice(request):
    # will show sales invoices
    return HttpResponse('List of sales invoices')

