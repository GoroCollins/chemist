from django import forms
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from . models import (Item, ItemEntry, Unit, Vendor, PurchaseHeader, PurchaseLine, PurchaseCreditMemoHeader, PurchaseCreditMemoLine, SalesHeader, 
                      SalesLines, SalesCreditMemoHeader, SalesCreditMemoLine)


class SalesHeaderForm(forms.ModelForm):
    class Meta:
        model = SalesHeader
        fields = ['customer']

class SalesLinesForm(forms.ModelForm):
    class Meta:
        model = SalesLines
        fields = ['item', 'lpo', 'quantity', 'discount']

SalesLinesFormset = forms.inlineformset_factory(SalesHeader, SalesLines, form=SalesLinesForm, can_delete=True, can_delete_extra=True, extra=1)

class SalesLinesUpdateForm(forms.ModelForm):
    class Meta:
        model = SalesLines 
        fields = ['item', 'lpo', 'quantity', 'discount']

SalesLineUpdateFormset = forms.inlineformset_factory(SalesHeader, SalesLines, form=SalesLinesUpdateForm, can_delete=False, extra=0)

class PurchaseHeaderForm(forms.ModelForm):
    class Meta:
        model = PurchaseHeader
        fields = ['vendor']

class PurchaseLineForm(forms.ModelForm):
    class Meta:
        model = PurchaseLine
        fields = ['item', 'quantity_requested', 'unit_price']

PurchaseLineFormset = forms.inlineformset_factory(PurchaseHeader, PurchaseLine, form=PurchaseLineForm, can_delete=True, can_delete_extra=True, extra=1)

class PurchaseLineReceivingForm(forms.ModelForm):
    class Meta:
        model = PurchaseLine
        fields = ['quantity_received', 'batch', 'expiry_date', 'markup', 'invoice_no']

PurchaseLineReceivingFormset = forms.inlineformset_factory(PurchaseHeader, PurchaseLine, form=PurchaseLineReceivingForm, can_delete=False,extra=0)

class SalesCreditMemoHeaderForm(forms.ModelForm):
    class Meta:
        model = SalesCreditMemoHeader
        fields = ['invoice_no']

class SalesCreditMemoLineForm(forms.ModelForm):
    class Meta:
        model = SalesCreditMemoLine
        fields = ['sales_line', 'quantity']

SalesCreditMemoLineFormset = forms.inlineformset_factory(SalesCreditMemoHeader, SalesCreditMemoLine, form=SalesCreditMemoLineForm, extra=1)

class PurchaseCreditMemoHeaderForm(forms.ModelForm):
    class Meta:
        model = PurchaseCreditMemoHeader
        fields = ['vendor']

class PurchaseCreditMemoLineForm(forms.ModelForm):
    class Meta:
        model = PurchaseCreditMemoLine
        fields = ['purchase_line','quantity']

PurchaseCreditMemoLineFormset = forms.inlineformset_factory(PurchaseCreditMemoHeader, PurchaseCreditMemoLine, form=PurchaseCreditMemoLineForm, extra=1)





