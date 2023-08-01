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
from . forms import (SalesHeaderForm, SalesLinesForm, PurchaseHeaderForm, PurchaseLineForm, SalesLinesFormset)
# Create your views here.

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

class SalesInvoiceListView(generic.ListView, LoginRequiredMixin):
    model = SalesHeader
    paginate_by = 25

class SalesInvoiceDetailView(generic.DetailView, LoginRequiredMixin):
    model = SalesHeader
    paginate_by = 25

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

class PurchaseCreditMemoListView(generic.ListView, LoginRequiredMixin):
    model = PurchaseCreditMemoHeader
    paginate_by = 25

class PurchaseCreditMemoDetailView(generic.DetailView, LoginRequiredMixin):
    model = PurchaseCreditMemoHeader

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
            url = reverse_lazy('invoice-detail', args=[str(line_instance.number)])
            return redirect(url)

    else:
        header_form = SalesHeaderForm(prefix='header')
        lines_formset = SalesLinesFormSet(prefix='lines')

    context = {
        'header_form': header_form,
        'lines_formset': lines_formset,
    }
    return render(request, 'inventory/sales_order.html', context)

# def purchase_order(request):
#     PurchaseLinesFormSet = forms.formset_factory(PurchaseLineForm, extra=1)

#     if request.method == 'POST':
#         header_form = PurchaseHeaderForm(request.POST, prefix='header')
#         lines_formset = PurchaseLinesFormSet(request.POST, prefix='lines')

#         if header_form.is_valid() and lines_formset.is_valid():
#             header_instance = header_form.save()
#             for form in lines_formset:
#                 line_instance = form.save(commit=False)
#                 line_instance.number = header_instance
#                 line_instance.save()

#             # Redirect to a success page or do something else
#             return redirect('purchaseorders')

#     else:
#         header_form = PurchaseHeaderForm(prefix='header')
#         lines_formset = PurchaseLinesFormSet(prefix='lines')

#     context = {
#         'header_form': header_form,
#         'lines_formset': lines_formset,
#     }
#     return render(request, 'inventory/purchase_order.html', context)

def purchase_order(request):
    PurchaseLinesFormSet = forms.formset_factory(PurchaseLineForm, extra=1)

    if request.method == 'POST':
        header_form = PurchaseHeaderForm(request.POST, prefix='header')
        lines_formset = PurchaseLinesFormSet(request.POST, prefix='lines')

        if header_form.is_valid() and lines_formset.is_valid():
            header_instance = header_form.save()

            # Process the lines formset
            for form in lines_formset:
                line_instance = form.save(commit=False)
                line_instance.number = header_instance

                # Check if the line_instance already exists
                if line_instance.pk:  # If it has a primary key, it's an existing instance
                    existing_line = PurchaseLine.objects.get(pk=line_instance.pk)
                    # Update the existing line with the form data
                    existing_line.item = line_instance.item
                    existing_line.batch = line_instance.batch
                    existing_line.quantity_requested = line_instance.quantity_requested
                    existing_line.unit_price = line_instance.unit_price
                    existing_line.expiry_date = line_instance.expiry_date
                    existing_line.quantity_received = line_instance.quantity_received
                    existing_line.invoice_no = line_instance.invoice_no
                    existing_line.save()
                else:
                    line_instance.save()  # It's a new line, so save it

            # Redirect to a success page or do something else
            url = reverse_lazy("purchaseorder-detail", args=[str(line_instance.number)])
            return redirect(url)

    else:
        header_form = PurchaseHeaderForm(prefix='header')
        lines_formset = PurchaseLinesFormSet(prefix='lines')

    context = {
        'header_form': header_form,
        'lines_formset': lines_formset,
    }
    return render(request, 'inventory/purchase_order.html', context)




