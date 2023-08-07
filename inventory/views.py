from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse, Http404
from .models import (Item, ItemEntry, PurchaseHeader, PurchaseLine, SalesHeader, SalesLines, Vendor, Unit, ApprovalEntry, SalesCreditMemoHeader, 
                     SalesCreditMemoLine, PurchaseCreditMemoHeader, PurchaseCreditMemoLine)
from django.views import generic
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from . forms import (SalesHeaderForm, PurchaseHeaderForm, SalesLinesFormset, PurchaseLineFormset,SalesCreditMemoHeaderForm, SalesCreditMemoLineFormset,
                     PurchaseCreditMemoHeaderForm, PurchaseCreditMemoLineFormset)
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
class VendorListView(generic.ListView, LoginRequiredMixin):
    model = Vendor
    paginate_by = 25

class VendorDetailView(generic.DetailView, LoginRequiredMixin):
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

class ItemListView(generic.ListView, LoginRequiredMixin):
    model = Item
    paginate_by = 25

class ItemDetailView(generic.DetailView, LoginRequiredMixin):
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

class PurchaseHeaderListView(generic.ListView, LoginRequiredMixin):
    model = PurchaseHeader
    paginate_by = 25

class PurchaseHeaderDetailView(generic.DetailView, LoginRequiredMixin):
    model = PurchaseHeader
    template_name = 'inventory/purchaseheader_detail.html'  # Ensure correct template name

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(PurchaseHeader, number=pk)

class PurchaseHeaderInline():
    form_class = PurchaseHeaderForm
    model = PurchaseHeader
    template_name = "inventory/purchase_order_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        url = reverse_lazy('inventory:purchaseorders')
        return redirect(url)
    
    def formset_purchaselines_valid(self, formset):
        purchaselines = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for purchaseline in purchaselines:
            purchaseline.number = self.object
            purchaseline.save()

class PurchaseOrderCreate(LoginRequiredMixin, PurchaseHeaderInline, generic.edit.CreateView):
    def get_context_data(self, **kwargs):
        context = super(PurchaseOrderCreate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context
    
    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'purchaselines': PurchaseLineFormset(prefix='lines'),
            }
        else:
            return {
                'purchaselines': PurchaseLineFormset(self.request.POST or None, prefix='lines'),
            }

class PurchaseOrderUpdate(LoginRequiredMixin, PurchaseHeaderInline, generic.edit.UpdateView):
    def get_context_data(self, **kwargs):
        context = super(PurchaseOrderUpdate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        return {
            'purchaselines': PurchaseLineFormset(self.request.POST or None,  instance=self.object, prefix='lines'),
        }
class SalesInvoiceListView(generic.ListView, LoginRequiredMixin):
    model = SalesHeader
    paginate_by = 25

class SalesInvoiceDetailView(generic.DetailView, LoginRequiredMixin):
    model = SalesHeader
    paginate_by = 25

class SalesHeaderInline():
    form_class = SalesHeaderForm
    model = SalesHeader
    template_name = "inventory/sales_invoice_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        url = reverse_lazy('inventory:invoices')
        return redirect(url)
    
    def formset_saleslines_valid(self, formset):
        saleslines = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for saleline in saleslines:
            saleline.number = self.object
            saleline.save()

class SalesInvoiceCreate(LoginRequiredMixin, SalesHeaderInline, generic.edit.CreateView):
    def get_context_data(self, **kwargs):
        context = super(SalesInvoiceCreate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context
    
    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'saleslines': SalesLinesFormset(prefix='lines'),
            }
        else:
            return {
                'saleslines': SalesLinesFormset(self.request.POST or None, prefix='lines'),
            }

class SalesInvoiceUpdate(LoginRequiredMixin, SalesHeaderInline, generic.edit.UpdateView):
    def get_context_data(self, **kwargs):
        context = super(SalesInvoiceUpdate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        return {
            'saleslines': SalesLinesFormset(self.request.POST or None,  instance=self.object, prefix='lines'),
        }

class ApprovalListView(generic.ListView, LoginRequiredMixin):
    model = ApprovalEntry
    paginate_by = 10

class ApprovalDetailView(generic.DetailView, LoginRequiredMixin):
    model = ApprovalEntry
    paginate_by =10

class SalesCreditMemoListView(generic.ListView, LoginRequiredMixin):
    model = SalesCreditMemoHeader
    paginate_by = 25

class SalesCreditMemoDetailView(generic.DetailView, LoginRequiredMixin):
    model = SalesCreditMemoHeader

class SalesCreditMemoHeaderInline():
    form_class = SalesCreditMemoHeaderForm
    model = SalesCreditMemoHeader
    template_name = "inventory/sales_memo_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        url = reverse_lazy('inventory:salesmemos')
        return redirect(url)
    
    def formset_salesmemolines_valid(self, formset):
        salesmemolines = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for salesmemoline in salesmemolines:
            salesmemoline.number = self.object
            salesmemoline.save()

class SalesCreditMemoCreate(LoginRequiredMixin, SalesCreditMemoHeaderInline, generic.edit.CreateView):
    def get_context_data(self, **kwargs):
        context = super(SalesCreditMemoCreate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context
    
    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'salesmemolines': SalesCreditMemoLineFormset(prefix='lines'),
            }
        else:
            return {
                'salesmemolines': SalesCreditMemoLineFormset(self.request.POST or None, prefix='lines'),
            }

class PurchaseCreditMemoListView(generic.ListView, LoginRequiredMixin):
    model = PurchaseCreditMemoHeader
    paginate_by = 25

class PurchaseCreditMemoDetailView(generic.DetailView, LoginRequiredMixin):
    model = PurchaseCreditMemoHeader

class PurchaseCreditMemoHeaderInline():
    form_class = PurchaseCreditMemoHeaderForm
    model = PurchaseCreditMemoHeader
    template_name = "inventory/purchase_memo_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        url = reverse_lazy('inventory:purchasememos')
        return redirect(url)
    
    def formset_purchasememolines_valid(self, formset):
        purchasememolines = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for purchasememoline in purchasememolines:
            purchasememoline.number = self.object
            purchasememoline.save()

class PurchaseCreditMemoCreate(LoginRequiredMixin, PurchaseCreditMemoHeaderInline, generic.edit.CreateView):
    def get_context_data(self, **kwargs):
        context = super(PurchaseCreditMemoCreate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context
    
    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'purchasememolines': PurchaseCreditMemoLineFormset(prefix='lines'),
            }
        else:
            return {
                'purchasememolines': PurchaseCreditMemoLineFormset(self.request.POST or None, prefix='lines'),
            }

class UnitCreateView(generic.edit.CreateView, LoginRequiredMixin):
    model = Unit
    fields = ['code', 'description']
    success_url = reverse_lazy("units")
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class UnitListView(generic.ListView, LoginRequiredMixin):
    model = Unit
    paginate_by = 25

class UnitDetailView(generic.DetailView, LoginRequiredMixin):
    model = Unit

class UnitUpdateView(generic.edit.UpdateView, LoginRequiredMixin):
    model = Unit
    fields = ['description']





