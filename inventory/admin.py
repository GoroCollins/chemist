from django.contrib import admin
from django import forms
# Change admin header
admin.site.site_header = 'Chemist Administration'
admin.site.index_title = 'Customization Interface'

# Register your models here.
from . models import Unit, Item, Vendor, PurchaseHeader, PurchaseLine, ItemEntry, SalesHeader, SalesLines

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
        ('Document Source',{"fields":["source_code",]})
        
    ]
    def has_delete_permission(self, request, obj = None):
        return False

admin.site.register(ItemEntry, ItemEntryAdmin)

class VendorAdmin(admin.ModelAdmin):
    list_display = ['code','description', 'kra_pin',]
    def has_delete_permission(self, request, obj = None):
        return False

admin.site.register(Vendor, VendorAdmin)

class SalesInline(admin.StackedInline):
    model = SalesLines
    extra = 1

class SalesLinesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Retrieve all batches associated with the selected item
        item = self.instance.item
        batches = ItemEntry.objects.filter(item=item).values_list('batch', flat=True).distinct()
        # Set choices for the batch field
        self.fields['batch'].choices = [(batch, batch) for batch in batches]

    class Meta:
        model = SalesLines
        fields = '__all__'
@admin.register(SalesHeader)
class SalesHeaderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Header Information', {"fields": ["customer"]}),
        
    ]
    inlines = [SalesInline]
    list_display = ('number', 'customer', 'amount', 'date')
    search_fields = ['number', 'customer', 'amount', 'date']
    list_filter = ['customer',  'date']
    # disable delete of model instances
    def has_delete_permission(self, request, obj = None):
        return False

