from django.contrib import admin
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
    list_display = ['entry_date','item', 'batch', 'quantity', 'expiry_date']
    list_filter = ['entry_date']
    def has_delete_permission(self, request, obj = None):
        return False

admin.site.register(ItemEntry, ItemEntryAdmin)

class VendorAdmin(admin.ModelAdmin):
    list_display = ['code','description', 'kra_pin',]
    def has_delete_permission(self, request, obj = None):
        return False

admin.site.register(Vendor, VendorAdmin)

