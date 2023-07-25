from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, Http404
from .models import Item, ItemEntry, PurchaseHeader, PurchaseLine, SalesHeader, SalesLines, Vendor, Unit, ApprovalEntry, SalesCreditMemoHeader, SalesCreditMemoLine, PurchaseCreditMemoHeader, PurchaseCreditMemoLine
from django.views import generic
from django.template import loader
from django.urls import reverse_lazy
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

class VendorCreateView(generic.edit.CreateView):
    model = Vendor
    fields = ['description', 'contact_email', 'contact_phone', 'address', 'kra_pin']
    success_url = reverse_lazy("vendors")

class VendorUpdateView(generic.edit.UpdateView):
    model = Vendor
    fields = ['contact_email', 'contact_phone', 'address']

class ItemListView(generic.ListView):
    model = Item
    paginate_by = 25

class ItemDetailView(generic.DetailView):
    model = Item
    paginate_by = 25

class ItemCreateView(generic.edit.CreateView):
    model = Item
    fields = ['code','description', 'unit']
    success_url = reverse_lazy("items")

class ItemUpdateView(generic.edit.UpdateView):
    model = Item
    fields = ['unit']

class PurchaseHeaderListView(generic.ListView):
    model = PurchaseHeader
    paginate_by = 25

class PurchaseHeaderDetailView(generic.DetailView):
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

class ApprovalDetailView(generic.DetailView):
    model = ApprovalEntry
    paginate_by =10

class SalesCreditMemoListView(generic.ListView):
    model = SalesCreditMemoHeader
    paginate_by = 25

class SalesCreditMemoDetailView(generic.DetailView):
    model = SalesCreditMemoHeader

class PurchaseCreditMemoListView(generic.ListView):
    model = PurchaseCreditMemoHeader
    paginate_by = 25

class PurchaseCreditMemoDetailView(generic.DetailView):
    model = PurchaseCreditMemoHeader

class UnitCreateView(generic.edit.CreateView):
    model = Unit
    fields = ['code', 'description']
    success_url = reverse_lazy("units")
    
class UnitListView(generic.ListView):
    model = Unit
    paginate_by = 25

class UnitDetailView(generic.DetailView):
    model = Unit

class UnitUpdateView(generic.edit.UpdateView):
    model = Unit
    fields = ['description']



