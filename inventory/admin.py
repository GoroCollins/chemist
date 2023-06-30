from django.contrib import admin

# Register your models here.
from . models import Unit, Item, Vendor, PurchaseHeader, PurchaseLine

class UnitAdmin(admin.ModelAdmin):
    fieldsets = [(None, {"fields": ["code"]}), ('Unit information', {"fields": ["description"]}),]


admin.site.register(Unit, UnitAdmin)
admin.site.register(Item)
admin.site.register(Vendor)

class LineInline(admin.StackedInline):
    model = PurchaseLine
    #extra = 3


class PurchaseHeaderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Header Information', {"fields": ["vendor"]}),
        
    ]
    inlines = [LineInline]


admin.site.register(PurchaseHeader, PurchaseHeaderAdmin)
