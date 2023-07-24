from django import forms
from django.utils.translation import gettext_lazy as _
from . models import Item, ItemEntry, Unit, Vendor, PurchaseHeader, PurchaseLine, PurchaseCreditMemoHeader, PurchaseCreditMemoLine, SalesHeader, SalesLines, SalesCreditMemoHeader, SalesCreditMemoLine

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['code', 'description']
        labels = {'code': _('Code'), 
                  'description':_('Description')}
        error_messages = {'code': {'max_length': _('The code value is too long')},
                          'description':{'max_length':_('The description is too long')}}
