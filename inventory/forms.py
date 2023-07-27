from django import forms
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from . models import Item, ItemEntry, Unit, Vendor, PurchaseHeader, PurchaseLine, PurchaseCreditMemoHeader, PurchaseCreditMemoLine, SalesHeader, SalesLines, SalesCreditMemoHeader, SalesCreditMemoLine


class SalesHeaderForm(forms.ModelForm):
    model = SalesHeader
    fields = ['customer',]

class SalesLinesForm(forms.ModelForm):
    model = SalesLines
    fields = ['item', 'lpo', 'quantity', 'discount']


def sales_order(request):
    SalesLinesFormSet = forms.formset_factory(SalesLinesForm, extra=1)  # You can set 'extra' to determine the number of SalesLines forms to display
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
    else:
        header_form = SalesHeaderForm(prefix='header')
        lines_formset = SalesLinesFormSet(prefix='lines')
    
    context = {
        'header_form': header_form,
        'lines_formset': lines_formset,
    }
    return render(request, 'sales_order.html', context)


