from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, Http404
from .models import Item, ItemEntry, PurchaseHeader, PurchaseLine, SalesHeader, SalesLines, Vendor, Unit, ApprovalEntry
from django.views import generic
from django.template import loader
# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_items = Item.objects.count()
    num_vendors = Vendor.objects.count()
    num_invoices = SalesHeader.objects.count()
    num_lpos = PurchaseHeader.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_items': num_items,
        'num_vendors': num_vendors,
        'num_invoices': num_invoices,
        'num_lpos': num_lpos,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'inventory/index.html', context=context)
class VendorListView(generic.ListView):
    model = Vendor

class VendorDetailView(generic.DetailView):
    model = Vendor

class ItemListView(generic.ListView):
    model = Item

class ItemDetailView(generic.DetailView):
    model = Item

class PurchaseOrderListView(generic.DetailView):
    model = PurchaseHeader

class PurchaseOrderDetailView(generic.DetailView):
    model = PurchaseHeader

class SalesInvoiceListView(generic.ListView):
    model = SalesHeader

class SalesInvoiceDetailView(generic.DetailView):
    model = SalesHeader

class ApprovalListView(generic.ListView):
    model = ApprovalEntry




