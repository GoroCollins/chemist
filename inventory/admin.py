from django.contrib import admin
from django import forms

# Change admin header
admin.site.site_header = 'Chemist Administration'
admin.site.index_title = 'Customization Interface'

# Register your models here.
from . models import (Unit, Item, Vendor, PurchaseHeader, PurchaseLine, ItemEntry,  SalesHeader, SalesLine, 
                      SalesCreditMemoHeader, SalesCreditMemoLine, ApprovalSetup, Profile)

class UnitAdmin(admin.ModelAdmin):
    fieldsets = [(None, {"fields": ["code"]}), ('Unit information', {"fields": ["description"]}),]


admin.site.register(Unit, UnitAdmin)
admin.site.register(Item)


class LineInline(admin.StackedInline):
    model = PurchaseLine
    extra = 1


class PurchaseHeaderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Header Information', {"fields": ["vendor"]}),
        
    ]
    inlines = [LineInline]
    list_display = ('number', 'vendor', 'total', 'date')
    search_fields = ['number', 'vendor', 'total', 'date']
    list_filter = ['vendor',  'date']
    # disable delete of model instances
    def has_delete_permission(self, request, obj = None):
        return False


admin.site.register(PurchaseHeader, PurchaseHeaderAdmin)

class ItemEntryAdmin(admin.ModelAdmin):
    editable_list = ['quantity']
    list_display = ['entry_date','item', 'batch', 'quantity', 'expiry_date', 'is_expired']
    list_filter = ['entry_date', ]
    #fields = [ 'item', 'batch','quantity', ('cost', 'sale'),'source_code',]
    fieldsets = [
        ('Item Details', {"fields": ["item", "batch", "quantity",]}),
        ('Item Pricing', {"fields":[("cost","sale",)]}),
        ('Document Source',{"fields":["source_code","purchase_doc_no"]})
        
    ]
    def has_delete_permission(self, request, obj = None):
        return False

admin.site.register(ItemEntry, ItemEntryAdmin)

class VendorAdmin(admin.ModelAdmin):
    list_display = ['code','description', 'kra_pin',]
    def has_delete_permission(self, request, obj = None):
        return False

admin.site.register(Vendor, VendorAdmin)

class SalesLinesForm(forms.ModelForm):
    lpo = forms.ModelChoiceField(queryset=ItemEntry.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.lpo:
            self.fields['lpo'].initial = self.instance.lpo

    def clean(self):
        cleaned_data = super().clean()
        lpo = cleaned_data.get('lpo')
        if lpo:
            cleaned_data['unit_price'] = lpo.sale
        return cleaned_data

    class Meta:
        model = SalesLine
        fields = '__all__'

class SalesInline(admin.StackedInline):
    model = SalesLine
    extra = 1
    form = SalesLinesForm
@admin.register(SalesHeader)
class SalesHeaderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Header Information', {"fields": ["customer"]}),
        
    ]
    inlines = [SalesInline]
    list_display = ('number', 'customer', 'amount', 'date', 'finalize')
    search_fields = ['number', 'customer', 'amount', 'date']
    list_filter = ['customer',  'date', 'finalize']
    # disable delete of model instances
    def has_delete_permission(self, request, obj = None):
        return False

class SalesCreditMemoInline(admin.StackedInline):
    model = SalesCreditMemoLine
    extra = 1
@admin.register(SalesCreditMemoHeader)
class SalesCreditMemoHeaderAdmin(admin.ModelAdmin):
    inlines = [SalesCreditMemoInline]

class ApprovalSetupAdmin(admin.ModelAdmin):
    list_display = ('user', 'approver', 'modified_by')
admin.site.register(ApprovalSetup, ApprovalSetupAdmin)

admin.site.register(Profile)
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
# class EmployeeInline(admin.StackedInline):
#     model = Employee
#     can_delete = False
#     verbose_name_plural = "employee"


# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = [EmployeeInline]


# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)