from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, Http404
from .models import Item, ItemEntry, PurchaseHeader, PurchaseLine, SalesHeader, SalesLines, Vendor, Unit
from django.views.generic import ListView
from django.template import loader
# Create your views here.

def index(request):
    # will show items list
    item = Item.objects.values_list('code') # get item code to form link to item details
    context = {'item': item}
    template = loader.get_template('item.html')
    return HttpResponse(template.render(context, request))
def item_details(request, item_id):
    try:
        i = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404('Item does not exist')
    return HttpResponse(i)
class VendorListView(ListView):
    model = Vendor

def purchaseorder(request):
    # will show purchase orders
    return HttpResponse('List of purchase orders')

def salesinvoice(request):
    # will show sales invoices
    return HttpResponse('List of sales invoices')

from datetime import datetime

def greeting():
    # Get the current time
    current_time = timezone.now().time()
    # Convert the time to hours
    current_hour = current_time.hour
    # Determine the time category
    if 5 <= current_hour < 12:
        time_category = "morning"
    elif 12 <= current_hour < 17:
        time_category = "afternoon"
    elif 17 <= current_hour < 20:
        time_category = "evening"
    else:
        time_category = "night"
    return time_category
# Print the time category
# print("It's currently", time_category)
