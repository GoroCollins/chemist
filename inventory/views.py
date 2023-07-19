from django.shortcuts import render, get_object_or_404
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
    pending_lpo = PurchaseHeader.objects.filter(status=1).count()
    open_lpo = PurchaseHeader.objects.filter(status=0).count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_items': num_items,
        'num_vendors': num_vendors,
        'num_invoices': num_invoices,
        'num_lpos': num_lpos,
        'num_visits': num_visits,
        'pending_lpo': pending_lpo,
        'open_lpo': open_lpo,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'inventory/index.html', context=context)
class VendorListView(generic.ListView):
    model = Vendor
    paginate_by = 25

class VendorDetailView(generic.DetailView):
    model = Vendor
    paginate_by = 25

class ItemListView(generic.ListView):
    model = Item
    paginate_by = 25

class ItemDetailView(generic.DetailView):
    model = Item
    paginate_by = 25

class PurchaseOrderListView(generic.ListView):
    model = PurchaseHeader
    paginate_by = 25

class PurchaseOrderDetailView(generic.DetailView):
    model = PurchaseHeader
    template_name = 'inventory/purchaseheader_detail.html'  # Ensure correct template name

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(PurchaseHeader, number=pk)

class SalesInvoiceListView(generic.ListView):
    model = SalesHeader
    paginate_by = 25

class SalesInvoiceDetailView(generic.DetailView):
    model = SalesHeader
    paginate_by = 25

class ApprovalListView(generic.ListView):
    model = ApprovalEntry
    paginate_by = 10




