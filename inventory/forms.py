from django import forms
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from . models import (Item, ItemEntry, Unit, Vendor, PurchaseHeader, PurchaseLine, PurchaseCreditMemoHeader, PurchaseCreditMemoLine, SalesHeader, 
                      SalesLines, SalesCreditMemoHeader, SalesCreditMemoLine)
# Usersignup
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
 
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )


class SalesHeaderForm(forms.ModelForm):
    class Meta:
        model = SalesHeader
        fields = ['customer']

class SalesLinesForm(forms.ModelForm):
    class Meta:
        model = SalesLines
        fields = ['item', 'lpo', 'quantity', 'discount']

# Inline formset
SalesLinesFormset = forms.inlineformset_factory(SalesHeader, SalesLines, form=SalesLinesForm, can_delete=True, can_delete_extra=True, extra=1)

class PurchaseHeaderForm(forms.ModelForm):
    class Meta:
        model = PurchaseHeader
        fields = ['vendor']

class PurchaseLineForm(forms.ModelForm):
    class Meta:
        model = PurchaseLine
        fields = ['item', 'quantity_requested', 'unit_price']

PurchaseLineFormset = forms.inlineformset_factory(PurchaseHeader, PurchaseLine, form=PurchaseLineForm, can_delete=True, can_delete_extra=True, extra=1)

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





