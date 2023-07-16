from django.db import models
from phone_field import PhoneField
from crum import get_current_user
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import datetime
from django.urls import reverse

# Custom fieldtype
import re
from django.db import models
from django.utils import timezone

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
                    number = match.group(1)
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
    class Meta:
        verbose_name_plural ='Units Of Measure'

class Item(models.Model):
    code = models.CharField('Item Code', max_length=20, primary_key=True)
    description = models.CharField(max_length=200)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='Items', related_query_name='Items')
    def __str__(self) -> str:
        return self.description
    def get_absolute_url(self):
        """Returns the url to access a particular item instance"""
        return reverse('item-detail', args=[str(self.code)])
    class Meta:
        verbose_name_plural = 'Items'

class Vendor(models.Model):
    code = VendorCode('Vendor Code',primary_key=True, editable=False)
    description = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = PhoneField()
    address = models.CharField(max_length=200)
    kra_pin = models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.description
    def get_absolute_url(self):
        """Returns url to access a particular vendor instance"""
        return reverse('vendor-detail', args=[str(self.code)])
    class Meta:
        verbose_name_plural = 'Vendors'

class PurchaseHeader(models.Model):
    number = AlphanumericAutoField(primary_key=True, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='vendor', related_query_name='vendor')
    date = models.DateField(auto_now_add=True, editable=False)
    total = models.IntegerField(editable=False, default=0)
    last_modified_at = models.DateTimeField(auto_now=True, editable=False)
    approval_status = [(0, 'Open'), (1, 'Pending Approval'), (2, 'Approved'), (3, 'Cancelled Approval')]
    status = models.CharField(max_length=30, choices=approval_status, default=0)
    created_by = models.ForeignKey('auth.User', blank=True, null=True, default=None, on_delete=models.PROTECT, related_name='lpo', related_query_name='lpo',editable=False)
    modified_by = models.ForeignKey('auth.User', blank=True, null=True, default=None, on_delete=models.PROTECT, related_name='lpo_m', related_query_name='lpo_m',editable=False)

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
    def get_absolute_url(self):
        return reverse('purchaseorder-detail', args=[str(self.number)])
    class Meta:
        verbose_name_plural = 'Purchase Orders'
class PurchaseLine(models.Model):
    number = models.ForeignKey(PurchaseHeader, on_delete=models.CASCADE, related_name='lines', related_query_name='lines')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='lpo', related_query_name='lpo')
    batch = models.CharField('Item Batch Number',max_length=200)
    quantity_requested = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField('Unit Price')
    total = models.IntegerField(editable=False)
    expiry_date = models.DateField('Expiry date')
    quantity_received = models.PositiveIntegerField(default=0)
    invoice_no = models.CharField('Vendor Invoice Number',max_length=100, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            # Update existing instance
            if self.quantity_received > self.quantity_requested:
                raise ValidationError('You cannot receive more than requested')
            if not self.invoice_no:
                raise ValidationError('Enter vendor invoice number')

            # Update values of corresponding fields in ItemEntry
            item_entry = self.item_entry.first()
            item_entry.batch = self.batch
            item_entry.quantity = self.quantity_received
            item_entry.expiry_date = self.expiry_date
            item_entry.cost = self.unit_price
            item_entry.save()

        else:
            # Update the total value of the PurchaseLine
            self.total = self.quantity_requested * self.unit_price
            # Create a new instance of PurchaseLine
            super(PurchaseLine, self).save(*args, **kwargs)

            # Create a new instance of ItemEntry
            item_entry = ItemEntry.objects.create(
                purchase_doc_no=self,
                item=self.item,
                batch=self.batch,
                quantity=self.quantity_received,
                expiry_date=self.expiry_date,
                cost=self.unit_price
            )

            # Assign the created ItemEntry instance to the foreign key field
            #self.number = item_entry

            # Calculate the total value of PurchaseLine
            self.total = self.quantity_requested * self.unit_price

        super(PurchaseLine, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.number}'

@receiver(post_save, sender=PurchaseLine)
def update_lpo_total(sender, instance, created, **kwargs):
    if created:
        lpo_header = instance.number
        total_amount = lpo_header.lines.filter(number__total=0).aggregate(total=Sum('total'))['total']
        lpo_header.total = total_amount or 0
        lpo_header.save()

class ItemEntry(models.Model):
    entry_date = models.DateField(auto_now_add=True, editable=False)
    purchase_doc_no = models.ForeignKey(PurchaseLine, on_delete=models.PROTECT, related_name='item_entry', related_query_name='item_entry', null=True, verbose_name='Purchase Document Number')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='grn', related_query_name='grn')
    batch = models.CharField('Batch Number', max_length=200)
    quantity = models.IntegerField()
    expiry_date = models.DateField('Expiry Date')
    cost = models.IntegerField()
    sale = models.IntegerField()
    expiry_status = models.BooleanField(default=False)
    source_code = models.CharField(max_length=100)
    @property
    def is_expired(self):
        '''Check expiry of items'''
        return self.expiry_date <= datetime.date.today()
    def get_source_code(self):
        if self.purchase_doc_no:
            return 'PURCHASES'
        else:
            return 'RETURNS'
    def save(self, *args, **kwargs):
        self.expiry_status = self.is_expired
        self.sale = self.cost * 1.4
        self.source_code = self.get_source_code()
        if self.sale <= self.cost:
            raise ValidationError('Selling price must be higher than the buying prce')
        #entry = 
        super(ItemEntry, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return f'Item:{self.item} Batch:{self.batch}'
    class Meta:
        verbose_name_plural = 'Item Entries'

class SalesHeader(models.Model):
    number = SalesInvoice(primary_key=True,editable=False)
    customer = models.CharField(max_length=200)
    date = models.DateField(auto_now=True)
    amount = models.FloatField(editable=False, default=0)
    finalize = models.BooleanField(default=True)
    created_by = models.ForeignKey('auth.User', blank=True, null=True, default=None, on_delete=models.PROTECT, related_name='sales', related_query_name='sales',editable=False)
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        #self.modified_by = user
        super(SalesHeader, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return self.number
    def get_absolute_url(self):
        return reverse('invoice-detail', args=[str(self.number)])
    class Meta:
        verbose_name_plural = 'Sales Invoices'

class SalesLines(models.Model):
    number = models.ForeignKey(SalesHeader, on_delete=models.CASCADE, related_name='lines', related_query_name='lines')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='invoices', related_query_name='invoices')
    batch = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField()
    lpo = models.ForeignKey(ItemEntry, on_delete=models.PROTECT, related_name='sales', related_query_name='sales',  null=True)
    unit_price = models.IntegerField(editable=False)
    total = models.FloatField(editable=False)
    discount = models.IntegerField('Percentage Discount', default=0)

    def save(self, *args, **kwargs):
        if not self.unit_price:
            item_entry = self.lpo
            if item_entry:
                self.unit_price = item_entry.sale
                self.batch = item_entry.batch
                item_entry.quantity -= self.quantity
                if item_entry.quantity < 0:
                    raise ValidationError(f'{self.item} is out of stock')
                else:
                    item_entry.save()
        self.total = (self.quantity * self.unit_price) * (1- self.discount/100)
        super(SalesLines, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return f'{self.number}'
@receiver(post_save, sender=SalesLines)
def update_invoice_total(sender, instance, created, **kwargs):
    if created:
        sales_header = instance.number
        total_amount = sales_header.lines.aggregate(total=Sum('total'))['total']
        sales_header.amount = total_amount or 0
        sales_header.save()

class ApprovalEntry(models.Model):
    requester = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.PROTECT, related_name='requestor', related_query_name='requestor')
    document_number = models.ForeignKey(PurchaseHeader, on_delete=models.PROTECT, related_name='approval', related_query_name='approval')
    details = models.CharField(max_length=200)
    approval_status = [(0,'Open'), (1,'Pending Approval'), (2,'Approved'), (3,'Cancelled Approval')]
    status = models.CharField(max_length=20, choices=approval_status)
    approver = models.ForeignKey('auth.User', on_delete=models.PROTECT, blank=True, null=True, related_name='approver', related_query_name='approver')
    amount = models.ForeignKey(PurchaseHeader, on_delete=models.PROTECT, related_name='approval_amount', related_query_name='approval_amount')
    request_date = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', blank=True, null=True, default=None, on_delete=models.PROTECT, related_name='modifier', related_query_name='modifier',editable=False)
    due_date = models.DateField(default=timezone.now)
    overdue = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.requester}-{self.document_number}: {self.details}'
    def get_absolute_url(self):
        return reverse('approval-detail', args=[str(self.id)])





