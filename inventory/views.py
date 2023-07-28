from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse, Http404
from .models import Item, ItemEntry, PurchaseHeader, PurchaseLine, SalesHeader, SalesLines, Vendor, Unit, ApprovalEntry, SalesCreditMemoHeader, SalesCreditMemoLine, PurchaseCreditMemoHeader, PurchaseCreditMemoLine
from django.views import generic
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from . forms import SalesHeaderForm, SalesLinesForm, PurchaseHeaderForm, PurchaseLineForm
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

class VendorCreateView(generic.edit.CreateView, LoginRequiredMixin):
    model = Vendor
    fields = ['description', 'contact_email', 'contact_phone', 'address', 'kra_pin']
    success_url = reverse_lazy("vendors")
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class VendorUpdateView(generic.edit.UpdateView, LoginRequiredMixin):
    model = Vendor
    fields = ['contact_email', 'contact_phone', 'address']

class ItemListView(generic.ListView):
    model = Item
    paginate_by = 25

class ItemDetailView(generic.DetailView):
    model = Item
    paginate_by = 25

class ItemCreateView(generic.edit.CreateView, LoginRequiredMixin):
    model = Item
    fields = ['code','description', 'unit']
    success_url = reverse_lazy("items")
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ItemUpdateView(generic.edit.UpdateView, LoginRequiredMixin):
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

class UnitCreateView(generic.edit.CreateView, LoginRequiredMixin):
    model = Unit
    fields = ['code', 'description']
    success_url = reverse_lazy("units")
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class UnitListView(generic.ListView):
    model = Unit
    paginate_by = 25

class UnitDetailView(generic.DetailView):
    model = Unit

class UnitUpdateView(generic.edit.UpdateView, LoginRequiredMixin):
    model = Unit
    fields = ['description']


def sales_order(request):
    SalesLinesFormSet = forms.formset_factory(SalesLinesForm, extra=1)

    if request.method == 'POST':
        header_form = SalesHeaderForm(request.POST, prefix='header')
        lines_formset = SalesLinesFormSet(request.POST, prefix='lines')

        if header_form.is_valid() and lines_formset.is_valid():
            header_instance = header_form.save()
            for form in lines_formset:
                line_instance = form.save(commit=False)
                line_instance.number = header_instance
                line_instance.save()

            # Redirect to a success page or do something else
            return redirect('invoices')

    else:
        header_form = SalesHeaderForm(prefix='header')
        lines_formset = SalesLinesFormSet(prefix='lines')

    context = {
        'header_form': header_form,
        'lines_formset': lines_formset,
    }
    return render(request, 'inventory/sales_order.html', context)

def purchase_order(request):
    PurchaseLinesFormSet = forms.formset_factory(PurchaseLineForm, extra=1)

    if request.method == 'POST':
        header_form = PurchaseHeaderForm(request.POST, prefix='header')
        lines_formset = PurchaseLinesFormSet(request.POST, prefix='lines')

        if header_form.is_valid() and lines_formset.is_valid():
            header_instance = header_form.save()
            for form in lines_formset:
                line_instance = form.save(commit=False)
                line_instance.number = header_instance
                line_instance.save()

            # Redirect to a success page or do something else
            return redirect('purchaseorders')

    else:
        header_form = PurchaseHeaderForm(prefix='header')
        lines_formset = PurchaseLinesFormSet(prefix='lines')

    context = {
        'header_form': header_form,
        'lines_formset': lines_formset,
    }
    return render(request, 'inventory/purchase_order.html', context)



