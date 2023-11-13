from django.db import models
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse, Http404, JsonResponse, FileResponse, StreamingHttpResponse, HttpResponseBadRequest
from django.contrib import messages
from .models import (Item, ItemEntry, PurchaseHeader, PurchaseLine, SalesHeader, SalesLines, Vendor, Unit, ApprovalEntry, SalesCreditMemoHeader, 
                     SalesCreditMemoLine, PurchaseCreditMemoHeader, PurchaseCreditMemoLine, Profile, ApprovalSetup)
from django.views import generic, View
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django import forms
from . forms import (SalesHeaderForm, PurchaseHeaderForm, SalesLinesFormset, PurchaseLineFormset,SalesCreditMemoHeaderForm, SalesCreditMemoLineFormset,
                     PurchaseCreditMemoHeaderForm, PurchaseCreditMemoLineFormset, PurchaseLineReceivingFormset, SalesLineUpdateFormset, ApprovalEntryForm)
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.templatetags.static import static
from django.contrib.staticfiles import finders
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer, PageTemplate
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.frames import Frame
from django.db.models import Sum
import csv
from django.core.exceptions import ObjectDoesNotExist


@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_items = Item.objects.count()
    num_vendors = Vendor.objects.count()
    num_invoices = SalesHeader.objects.count()
    num_lpos = PurchaseHeader.objects.count()
    pending_lpo = PurchaseHeader.objects.filter(status=1).count()
    open_lpo = PurchaseHeader.objects.filter(status=0).count()
    total_sales = SalesHeader.objects.aggregate(total=Sum('amount'))['total']
    open_lpo_value = PurchaseHeader.objects.filter(status=0).aggregate(total=Sum('total'))['total']
    released_lpos = PurchaseHeader.objects.filter(status=2).aggregate(total=Sum('total'))['total']
    pending_lpo_value = PurchaseHeader.objects.filter(status=1).aggregate(total=Sum('total'))['total']
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
        'total_sales': total_sales,
        'open_lpo_value': open_lpo_value,
        'released_lpos': released_lpos,
        'pending_lpo_value': pending_lpo_value
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'inventory/index.html', context=context)
@login_required
def cancelled_documents(request):
    lpos = PurchaseHeader.objects.filter(status=3)
    context = {
        'lpos': lpos
    }
    return render(request, 'inventory/cancelled.html', context=context)
class VendorListView(LoginRequiredMixin, generic.ListView):
    model = Vendor
    paginate_by = 25

class VendorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Vendor
    paginate_by = 25

class VendorCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Vendor
    fields = ['description', 'contact_email', 'contact_phone', 'address', 'kra_pin']
    success_url = reverse_lazy("vendors")
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class VendorUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Vendor
    fields = ['contact_email', 'contact_phone', 'address']

class ItemListView(LoginRequiredMixin, generic.ListView):
    model = Item
    paginate_by = 25

class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = Item
    paginate_by = 25

class ItemCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Item
    fields = ['code','description', 'unit']
    success_url = reverse_lazy("items")
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Item
    fields = ['unit']

class PurchaseHeaderListView(LoginRequiredMixin, generic.ListView):
    model = PurchaseHeader
    paginate_by = 25

class PurchaseHeaderDetailView(LoginRequiredMixin, generic.DetailView):
    model = PurchaseHeader
    template_name = 'inventory/purchaseheader_detail.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(PurchaseHeader, number=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context

    def post(self, request, pk):
        if request.method == 'POST':
            purchase_header = self.get_object()
            amount = purchase_header.total
            
            approval_entries = ApprovalEntry.objects.filter(document_number=purchase_header).order_by('-request_date')
            if approval_entries and approval_entries[0].status==1:
                approval_entry = approval_entries[0]
                approval_entry.status = 0
                approval_entry.save()
                messages.success(request, 'Approval request cancelled')
                return redirect('inventory:purchaseorder-detail', pk=pk)
            else:
                if pk and amount:
                    try:
                        approver_setup = ApprovalSetup.objects.get(user=request.user)
                        approver = approver_setup.approver
                    except ApprovalSetup.DoesNotExist:
                        approver = None 
                    
                    ApprovalEntry.objects.create(
                        requester=request.user,
                        document_number=purchase_header,
                        details="Your details here",
                        amount=amount, 
                        approver=approver,
                        request_date=timezone.now()
                    )
                    messages.success(request, 'Approval request sent')
                    return redirect('inventory:purchaseorder-detail', pk=pk)
                    # return JsonResponse({'message': 'Approval request sent'})
                else:
                    messages.error(request, 'Missing document_number or amount')
                    return redirect('inventory:purchaseorder-detail', pk=pk)
                    #return JsonResponse({'error': 'Missing document_number or amount'}, status=400)
        else:
            messages.error(request, 'Invalid request method')
            return redirect('inventory:purchaseorder-detail', pk=pk)
            #return JsonResponse({'error': 'Invalid request method'}, status=400)

class PurchaseHeaderInline():
    form_class = PurchaseHeaderForm
    model = PurchaseHeader
    template_name = "inventory/purchase_order_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        url = reverse_lazy('inventory:purchaseorder-detail', kwargs={'pk': str(self.object.pk)})
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

class PurchaseHeaderReceivingInline():
    form_class = PurchaseHeaderForm
    model = PurchaseHeader
    template_name = "inventory/purchase_order_receive.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        url = reverse_lazy('inventory:purchaseorder-detail', kwargs={'pk': str(self.object.pk)})
        return redirect(url)
    
    def formset_purchaselines_valid(self, formset):
        purchaselinesreceive = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for purchaseline in purchaselinesreceive:
            purchaseline.number = self.object
            purchaseline.save()

class PurchaseOrderReceive(LoginRequiredMixin, PurchaseHeaderReceivingInline, generic.edit.UpdateView):
    def get_context_data(self, **kwargs):
        context = super(PurchaseOrderReceive, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        context['is_update'] = True
        return context

    def get_named_formsets(self):
        return {
            'purchaselinesreceive': PurchaseLineReceivingFormset(self.request.POST or None,  instance=self.object, prefix='lines'),
        }
class SalesInvoiceListView(LoginRequiredMixin, generic.ListView):
    model = SalesHeader
    paginate_by = 25

class SalesInvoiceDetailView(LoginRequiredMixin, generic.DetailView):
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
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        url = reverse_lazy('inventory:invoice-detail', kwargs={'pk': str(self.object.pk)})
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

class SalesHeaderUpdateInline():
    form_class = SalesHeaderForm
    model = SalesHeader
    template_name = "inventory/sales_invoice_update.html"

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
        url = reverse_lazy('inventory:invoice-detail', kwargs={'pk': str(self.object.pk)})
        return redirect(url)
    
    def formset_saleslines_valid(self, formset):
        saleslinesupdate = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for saleline in saleslinesupdate:
            saleline.number = self.object
            saleline.save()

class SalesInvoiceUpdate(LoginRequiredMixin, SalesHeaderUpdateInline, generic.edit.UpdateView):
    def get_context_data(self, **kwargs):
        context = super(SalesInvoiceUpdate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        context['messages'] = messages.get_messages(self.request)
        context['is_update'] = True
        return context
    def get_named_formsets(self):
        return {
            'saleslinesupdate': SalesLineUpdateFormset(self.request.POST or None,  instance=self.object, prefix='lines'),
        }


    def get(self, request, *args, **kwargs):
        # Call the parent get method to retrieve the object
        self.object = self.get_object()
        
        # Check if the invoice has been finalized
        if self.object.finalize == 1:
            
            # Display a message using the messages framework
            invoice_number = self.object.number
            messages.warning(self.request, f"The invoice: {invoice_number} has been finalized.")

            # Clear messages after using them
            messages.get_messages(self.request).used = True
            
            # Redirect the user to the invoice-detail page
            url = reverse_lazy('inventory:invoice-detail', kwargs={'pk': invoice_number})
            return redirect(url)
        formset = self.get_named_formsets()['saleslinesupdate']
        
        return super().get(request, *args, **kwargs)

class ApprovalListView(LoginRequiredMixin, generic.ListView):
    model = ApprovalEntry
    paginate_by = 30

class ApprovalDetailView(LoginRequiredMixin, generic.DetailView):
    model = ApprovalEntry
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context
    def post(self, request, pk):
        approval_entry = ApprovalEntry.objects.filter(pk=pk).first()
    
        if approval_entry is not None:
            if 'action' in request.POST:
                action = request.POST['action']
        
                if action == 'approve':
                    approval_entry.status = 2
                    message = 'Approval entry approved'
                elif action == 'reject':
                    approval_entry.status = 3
                    message = 'Approval entry rejected'
                    return redirect('inventory:approval-update', pk=pk)
                else:
                    messages.error(request, 'Invalid action')
                    return redirect('inventory:approval-detail', pk=pk)

                approval_entry.save()
                messages.success(request, message)
                return redirect('inventory:approval-detail', pk=pk)
            else:
                messages.error(request, 'Action parameter missing')
                return redirect('inventory:approval-detail', pk=pk)
        else:
            messages.error(request, 'Error processing request')
            return redirect('inventory:approval-detail', pk=pk)

class ApprovalUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ApprovalEntry
    fields = ['reason']

class SalesCreditMemoListView(LoginRequiredMixin, generic.ListView):
    model = SalesCreditMemoHeader
    paginate_by = 25

class SalesCreditMemoDetailView(LoginRequiredMixin, generic.DetailView):
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
        url = reverse_lazy('inventory:salesmemo-detail', kwargs={'pk': str(self.object.pk)})
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

class PurchaseCreditMemoListView(LoginRequiredMixin, generic.ListView):
    model = PurchaseCreditMemoHeader
    paginate_by = 25

class PurchaseCreditMemoDetailView(LoginRequiredMixin, generic.DetailView):
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
        url = reverse_lazy('inventory:purchasememo-detail', kwargs={'pk': str(self.object.pk)})
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

class UnitCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Unit
    fields = ['code', 'description']
    success_url = reverse_lazy("inventory:units")
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class UnitListView(generic.ListView, LoginRequiredMixin):
    model = Unit
    paginate_by = 25

class UnitDetailView(LoginRequiredMixin, generic.DetailView):
    model = Unit

class UnitUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Unit
    fields = ['description']

class UserProfile(View):
    template_name = 'inventory/profile.html'

    def get(self, request):
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user_profile = None
        form_data = {
            'name': user_profile.full_name if user_profile else '',
            'email': request.user.email if user_profile else '', 
            'designation': user_profile.designation if user_profile else '',
            'mobile_no': user_profile.mobile_number if user_profile else '',
            'profile_image': user_profile.profile_image if user_profile else '',
            'profile_summary': user_profile.profile_summary if user_profile else '',
            'city': user_profile.city if user_profile else '',
            'state': user_profile.state if user_profile else '',
            'country': user_profile.country if user_profile else '',
        }
        context = {
        'profile': user_profile,
        'form_data': form_data
        }
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user_profile = None
        uploaded_image = request.FILES.get('profile_image', None)
        if uploaded_image:
            user_profile.profile_image.save(uploaded_image.name, ContentFile(uploaded_image.read()))
        full_name = request.POST.get('name')
        email = request.POST.get('email') 
        designation = request.POST.get('designation')
        mobile_number = request.POST.get('mobile_no')
        profile_summary = request.POST.get('profile_summary')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        if user_profile:
            user_profile.full_name = full_name
            user_profile.designation = designation
            user_profile.mobile_number = mobile_number
            user_profile.profile_summary = profile_summary
            user_profile.city = city
            user_profile.state = state
            user_profile.country = country
            user_profile.save()

       
            user_profile.user.email = email
            user_profile.user.save()

        return redirect('inventory:home') 
class ApprovalSetupListView(LoginRequiredMixin, generic.ListView):
    model = ApprovalSetup
    paginate_by = 25

class ApprovalSetupCreateView(LoginRequiredMixin, generic.CreateView):
    model = ApprovalSetup
    fields = ['user', 'approver']
    success_url = reverse_lazy("inventory:approvalsetup")
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ApprovalSetupUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ApprovalSetup
    fields = ['approver']
class ApprovalSetupDetailView(LoginRequiredMixin, generic.DetailView):
    model = ApprovalSetup

def sales_pdf(request, pk):
    # Create a response object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="invoice_{pk}.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=A4)

    # Create a list of data for the table
    data = [['Item', 'Batch Number', 'Quantity', 'Unit Price', 'Discount', 'Line Amount']]
    sales_header = get_object_or_404(SalesHeader, pk=pk)
    # Fetch related sales lines
    sales_lines = SalesLines.objects.filter(number=sales_header)
    for row in sales_lines:
        data.append([row.item, row.batch, row.quantity, row.unit_price, row.discount, row.total])
        # Create a list to hold the elements (text, image, and table)
    elements = []

    # Load and add an image to the top-right frame
    image_path = '/home/goro/projects/inventory/chemist/inventory/static/inventory/images/mypic.png'  # Replace with the actual path to your image
    img = Image(image_path, width=200, height=100)  # Adjust width and height as needed
    img.hAlign = 'RIGHT'  # Align the image to the right within the frame

    elements.append(img)

    # Add information from SalesHeader above the table
    elements.append(Paragraph(f"Invoice Number: {sales_header.number}", getSampleStyleSheet()["Title"]))
    elements.append(Paragraph(f"Customer Name: {sales_header.customer}", getSampleStyleSheet()["Title"]))
    elements.append(Paragraph(f"Total Amount: Ksh. {sales_header.amount}", getSampleStyleSheet()["Title"]))
    elements.append(Paragraph(f"Invoice Date: {sales_header.date}", getSampleStyleSheet()["Title"]))

    # Add a spacer to create some space between the information and the table
    elements.append(Spacer(1, 12))

    # Create a table and set its style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF document
    elements.append(table)
    # doc.addPageTemplates(page_template)
    doc.build(elements)
    return response

def purchases_pdf(request, pk):
    # Create a response object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="LPO_{pk}.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=A4)

    # Create a list of data for the table
    data = [['Item', 'Batch Number', 'Quantity Requested', 'Unit Price', 'Line Amount']]
    purchase_header = get_object_or_404(PurchaseHeader, pk=pk)
    # Fetch related sales lines
    purchase_lines = PurchaseLine.objects.filter(number=purchase_header)
    for row in purchase_lines:
        data.append([row.item, row.batch, row.quantity_requested, row.unit_price,  row.total])
        # Create a list to hold the elements (text, image, and table)
    elements = []

    # Load and add an image to the top-right frame
    image_path = '/home/goro/projects/inventory/chemist/inventory/static/inventory/images/mypic.png'  # Replace with the actual path to your image
    img = Image(image_path, width=200, height=100)  # Adjust width and height as needed
    img.hAlign = 'RIGHT'  # Align the image to the right within the frame

    elements.append(img)

    # Add information from SalesHeader above the table
    elements.append(Paragraph(f"Purchase Order Number: {purchase_header.number}", getSampleStyleSheet()["Title"]))
    elements.append(Paragraph(f"Vendor Name: {purchase_header.vendor}", getSampleStyleSheet()["Title"]))
    elements.append(Paragraph(f"Purchase Order Amount: Ksh. {purchase_header.total}", getSampleStyleSheet()["Title"]))
    elements.append(Paragraph(f"Purchase Order Date: {purchase_header.date}", getSampleStyleSheet()["Title"]))

    # Add a spacer to create some space between the information and the table
    elements.append(Spacer(1, 12))

    # Create a table and set its style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF document
    elements.append(table)
    # doc.addPageTemplates(page_template)
    doc.build(elements)
    return response

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value





