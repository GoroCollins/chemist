from django.db import models
from phone_field import PhoneField
from crum import get_current_user
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


## Custom fieldtype
import re
from django.db import models
from django.utils import timezone

# Custom fields
class AlphanumericAutoField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15  # Maximum length of the alphanumeric value
        kwargs['unique'] = True    # Ensure uniqueness of the field
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            current_year = timezone.now().year

            # Retrieve the latest alphanumeric value from the table for the current year
            latest_value = model_instance.__class__.objects.filter(
                **{self.attname + '__startswith': 'LPO' + str(current_year)}
            ).order_by('-number').values_list(self.attname, flat=True).first()

            if latest_value:
                # Extract the prefix, year, and number components from the latest value
                match = re.match(r'LPO(\d+)/(\d+)', latest_value)
                if match:
                    year = match.group(1)
                    number = match.group(2)
                    new_number = int(number) + 1
                    new_value = f'LPO{year}/{new_number:05d}'
                else:
                    # Invalid format, fallback to initial value
                    new_value = f'LPO{current_year}/00001'
            else:
                new_value = f'LPO{current_year}/00001'

            setattr(model_instance, self.attname, new_value)

        return super().pre_save(model_instance, add)


class SalesInvoice(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15  # Maximum length of the alphanumeric value
        kwargs['unique'] = True    # Ensure uniqueness of the field
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            current_year = timezone.now().year

            # Retrieve the latest alphanumeric value from the table for the current year
            latest_value = model_instance.__class__.objects.filter(
                **{self.attname + '__startswith': 'SINV' + str(current_year)}
            ).order_by('-number').values_list(self.attname, flat=True).first()

            if latest_value:
                # Extract the prefix, year, and number components from the latest value
                match = re.match(r'SINV(\d+)/(\d+)', latest_value)
                if match:
                    year = match.group(1)
                    number = match.group(2)
                    new_number = int(number) + 1
                    new_value = f'SINV{year}/{new_number:05d}'
                else:
                    # Invalid format, fallback to initial value
                    new_value = f'SINV{current_year}/00001'
            else:
                new_value = f'SINV{current_year}/00001'

            setattr(model_instance, self.attname, new_value)

        return super().pre_save(model_instance, add)

    
class VendorCode(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10  # Maximum length of the alphanumeric value
        kwargs['unique'] = True    # Ensure uniqueness of the field
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            

            # Retrieve the latest alphanumeric value from the table for the current year
            latest_value = model_instance.__class__.objects.filter(
                **{self.attname + '__startswith': 'V' }
            ).order_by('-code').values_list(self.attname, flat=True).first()

            if latest_value:
                # Extract the prefix, year, and number components from the latest value
                match = re.match(r'V-(\d+)', latest_value)
                if match:
                    number = match.group(2)
                    new_number = int(number) + 1
                    new_value = f'V-{new_number:05d}'
                else:
                    # Invalid format, fallback to initial value
                    new_value = f'V-00001'
            else:
                new_value = f'V-00001'

            setattr(model_instance, self.attname, new_value)

        return super().pre_save(model_instance, add)


# Create your models here.
class Unit(models.Model):
    code = models.CharField('Unit of measure code',max_length=10, primary_key=True)
    description = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.description

class Item(models.Model):
    code = models.CharField('Item Code', max_length=20, primary_key=True)
    description = models.CharField(max_length=200)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='Items', related_query_name='Items')
    def __str__(self) -> str:
        return self.description

class Vendor(models.Model):
    code = VendorCode('Vendor Code',primary_key=True, editable=False)
    description = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = PhoneField()
    address = models.CharField(max_length=200)
    kra_pin = models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.description

# class PurchaseOrder(models.Model):
#     number = AlphanumericAutoField(primary_key=True, editable=False)
#     vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='Vendors', related_query_name='vendor_code')
#     item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='Items', related_query_name='item_code')
#     batch = models.CharField('Item Batch Number',max_length=200)
#     quantity = models.PositiveIntegerField()
#     unit_price = models.PositiveIntegerField('Unit Price')
#     total = models.IntegerField(editable=False)
#     expiry_date = models.DateField('Expiry date')
#     created_at = models.DateTimeField(auto_now_add=True, editable=False)
#     last_modified_at = models.DateTimeField(auto_now=True, editable=False)
#     created_by = models.ForeignKey('auth.User', blank=True, null=True, default=None, on_delete=models.PROTECT, related_name='Create', related_query_name='Create',editable=False)
#     modified_by = models.ForeignKey('auth.User', blank=True, null=True, default=None, on_delete=models.PROTECT, related_name='Modify', related_query_name='Modify',editable=False)
#     @property
#     def total_price(self):
#         "Returns total price."
#         return self.quantity * self.unit_price
#     # def save(self, *args, **kwargs):
#     #     self.total = self.total_price
#     #     super(LPO, self).save(*args, **kwargs)
#     def save(self, *args, **kwargs):
#         self.total = self.quantity * self.unit_price
#         user = get_current_user()
#         if user and not user.pk:
#             user = None
#         if not self.pk:
#             self.created_by = user
#         self.modified_by = user
#         super(PurchaseOrder, self).save(*args, **kwargs)

#     def __str__(self) -> str:
#         return self.number
    
# class SalesHeader(models.Model):
#     number = SalesInvoice(primary_key=True,editable=False)
#     customer = models.CharField(max_length=200)
#     date = models.DateField(auto_now=True)
#     amount = models.IntegerField(editable=False)
#     def __str__(self) -> str:
#         return self.number

# class SalesLines(models.Model):
#     number = models.ForeignKey(SalesHeader, on_delete=models.CASCADE, related_name='lines', related_query_name='lines')
#     item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='invoices', related_query_name='invoices')
#     quantity = models.IntegerField()
#     price = models.IntegerField()
#     total = models.IntegerField()
#     def __str__(self) -> str:
#         return f'Sales Lines For {self.number}'
    
# class Stock(models.Model):
#     item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='Item', related_query_name='Item')

class PurchaseHeader(models.Model):
    number = AlphanumericAutoField(primary_key=True, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='vendor', related_query_name='vendor')
    date = models.DateField(auto_now_add=True, editable=False)
    total = models.IntegerField(editable=False, default=0)
    last_modified_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey('auth.User', blank=True, null=True, default=None, on_delete=models.PROTECT, related_name='Create', related_query_name='Create',editable=False)
    modified_by = models.ForeignKey('auth.User', blank=True, null=True, default=None, on_delete=models.PROTECT, related_name='Modify', related_query_name='Modify',editable=False)
    # @property
    # def total_price(self):
    #     "Returns total price."
    #     lpo_total = 0
    #     lpos = PurchaseHeader.objects.filter(total=0)
    #     lpo_number = lpos.number
    #     line_totals = lpo_number.Header.all()
    #     for line in line_totals:
    #         line_total = line.total
    #         lpo_total += line_total
    #     return lpo_total
    # def save(self, *args, **kwargs):
    #     self.total = self.total_price
    #     super(LPO, self).save(*args, **kwargs)
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user

        # if PurchaseHeader.objects.filter(total=0).exists():
        #     raise ValidationError("An incomplete LPO exists. Please fill the lines."
        super(PurchaseHeader, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.number
class PurchaseLine(models.Model):
    number = models.ForeignKey(PurchaseHeader, on_delete=models.CASCADE, related_name='lines', related_query_name='lines')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='lpo', related_query_name='lpo')
    batch = models.CharField('Item Batch Number',max_length=200)
    quantity_requested = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField('Unit Price')
    total = models.IntegerField(editable=False)
    expiry_date = models.DateField('Expiry date')
    quantity_received = models.PositiveIntegerField(default=0)
    # @property
    # def lpo_total(self):
    #     #line = PurchaseLine.objects.filter(number__total=0)[0]
    #     total_amount = PurchaseLine.objects.filter(number__total=0).aggregate(total=Sum('total'))['total']
    #     return total_amount
    def save(self, *args, **kwargs):
        self.total = self.quantity_requested * self.unit_price
        # total_amount = PurchaseLine.objects.filter(number__total=0).aggregate(total=Sum('total'))['total']
        # self.number.total = total_amount or 0
        self.number.save()
        super(PurchaseLine, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'Purchase Line For LPO:{self.number}'

# @receiver(post_save, sender=PurchaseLine)
# def update_lpo_total(sender, instance, created, **kwargs):
#     if created:
#         lpo_header = instance.number
#         total_amount = lpo_header.lines.filter(number__total=0).aggregate(total=Sum('total'))['total']
#         lpo_header.total = total_amount or 0
#         lpo_header.save()








