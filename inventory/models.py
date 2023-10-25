from django.db import models
from phone_field import PhoneField
from crum import get_current_user
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import datetime
from django.urls import reverse
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User, Permission
from PIL import Image
from django.contrib.auth import get_user_model # check it's usage
from django.contrib.contenttypes.models import ContentType

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
                match = re.match(r'LPO(\d+)-(\d+)', latest_value)
                if match:
                    year = match.group(1)
                    number = match.group(2)
                    new_number = int(number) + 1
                    new_value = f'LPO{year}-{new_number:05d}'
                else:
                    # Invalid format, fallback to initial value
                    new_value = f'LPO{current_year}-00001'
            else:
                new_value = f'LPO{current_year}-00001'

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
                match = re.match(r'SINV(\d+)-(\d+)', latest_value)
                if match:
                    year = match.group(1)
                    number = match.group(2)
                    new_number = int(number) + 1
                    new_value = f'SINV{year}-{new_number:05d}'
                else:
                    # Invalid format, fallback to initial value
                    new_value = f'SINV{current_year}-00001'
            else:
                new_value = f'SINV{current_year}-00001'

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
    
class SalesCreditMemo(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15  # Maximum length of the alphanumeric value
        kwargs['unique'] = True    # Ensure uniqueness of the field
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            current_year = timezone.now().year

            # Retrieve the latest alphanumeric value from the table for the current year
            latest_value = model_instance.__class__.objects.filter(
                **{self.attname + '__startswith': 'SCM' + str(current_year)}
            ).order_by('-number').values_list(self.attname, flat=True).first()

            if latest_value:
                # Extract the prefix, year, and number components from the latest value
                match = re.match(r'SCM(\d+)-(\d+)', latest_value)
                if match:
                    year = match.group(1)
                    number = match.group(2)
                    new_number = int(number) + 1
                    new_value = f'SCM{year}-{new_number:05d}'
                else:
                    # Invalid format, fallback to initial value
                    new_value = f'SCM{current_year}-00001'
            else:
                new_value = f'SCM{current_year}-00001'

            setattr(model_instance, self.attname, new_value)

        return super().pre_save(model_instance, add)

class PurchaseCreditMemo(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15  # Maximum length of the alphanumeric value
        kwargs['unique'] = True    # Ensure uniqueness of the field
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            current_year = timezone.now().year

            # Retrieve the latest alphanumeric value from the table for the current year
            latest_value = model_instance.__class__.objects.filter(
                **{self.attname + '__startswith': 'PCM' + str(current_year)}
            ).order_by('-number').values_list(self.attname, flat=True).first()

            if latest_value:
                # Extract the prefix, year, and number components from the latest value
                match = re.match(r'PCM(\d+)-(\d+)', latest_value)
                if match:
                    year = match.group(1)
                    number = match.group(2)
                    new_number = int(number) + 1
                    new_value = f'PCM{year}-{new_number:05d}'
                else:
                    # Invalid format, fallback to initial value
                    new_value = f'PCM{current_year}-00001'
            else:
                new_value = f'PCM{current_year}-00001'

            setattr(model_instance, self.attname, new_value)

        return super().pre_save(model_instance, add)


# Create your models here.
class Unit(models.Model):
    code = models.CharField('Unit of measure code',max_length=10, primary_key=True)
    description = models.CharField(max_length=200, verbose_name='Unit of Measure')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='units', related_query_name='units')
    def __str__(self) -> str:
        return self.description
    class Meta:
        verbose_name_plural ='Units Of Measure'
        ordering = ['code']
    def get_absolute_url(self):
        return reverse('inventory:unit-detail', args=[str(self.code)])

class Item(models.Model):
    code = models.CharField('Item Code', max_length=20, primary_key=True)
    description = models.CharField(max_length=200)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='Items', related_query_name='Items')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='useritems', related_query_name='useritems')
    def __str__(self) -> str:
        return self.description
    def get_absolute_url(self):
        """Returns the url to access a particular item instance"""
        return reverse('inventory:item-detail', args=[str(self.code)])
    class Meta:
        verbose_name_plural = 'Items'
        ordering = ["code"]

class Vendor(models.Model):
    code = VendorCode('Vendor Code',primary_key=True, editable=False)
    description = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = PhoneField()
    address = models.CharField(max_length=200)
    kra_pin = models.CharField(max_length=30)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='vendors', related_query_name='vendors')
    def __str__(self) -> str:
        return self.description
    def get_absolute_url(self):
        """Returns url to access a particular vendor instance"""
        return reverse('inventory:vendor-detail', args=[str(self.code)])
    class Meta:
        verbose_name_plural = 'Vendors'
        ordering = ["code"]

class PurchaseHeader(models.Model):
    number = AlphanumericAutoField(primary_key=True, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='vendor', related_query_name='vendor')
    date = models.DateField(auto_now_add=True, editable=False)
    total = models.DecimalField(editable=False, default=0, max_digits=10, decimal_places=2)
    last_modified_at = models.DateTimeField(auto_now=True, editable=False)
    approval_status = ((0, 'Open'), (1, 'Pending Approval'), (2, 'Approved'), (3, 'Cancelled Approval'))
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
        return reverse('inventory:purchaseorder-detail', args=[str(self.number)])
    class Meta:
        verbose_name_plural = 'Purchase Orders'
        ordering = ["number"]
class PurchaseLine(models.Model):
    number = models.ForeignKey(PurchaseHeader, on_delete=models.CASCADE, related_name='lines', related_query_name='lines')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='lpo', related_query_name='lpo')
    batch = models.CharField('Item Batch Number',max_length=200, null=True)
    quantity_requested = models.PositiveIntegerField(help_text='Quantity')
    unit_price = models.DecimalField('Unit Price', decimal_places=2, max_digits=10)
    total = models.DecimalField(editable=False, max_digits=10, decimal_places=2)
    expiry_date = models.DateField('Expiry date', null=True)
    quantity_received = models.PositiveIntegerField(default=0)
    markup = models.DecimalField(validators=[MaxValueValidator(100)], default=40, help_text="Percentage Markup", decimal_places=2, max_digits=6)
    invoice_no = models.CharField('Vendor Invoice Number',max_length=100, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            # Update existing instance
            if self.quantity_received > self.quantity_requested:
                raise ValidationError(f'You cannot receive more {self.quantity_requested} that were requested')
            if not self.invoice_no:
                raise ValidationError('Enter vendor invoice number')
            if not self.batch:
                raise ValidationError('Enter batch number')
            if not self.expiry_date:
                raise ValidationError('Enter expiry date')
            
            item_entry = ItemEntry.objects.create(
                purchase_doc_no=self,
                item=self.item,
                batch=self.batch,
                quantity=self.quantity_received,
                expiry_date=self.expiry_date,
                cost=self.unit_price,
                sale=self.unit_price * (1 + (self.markup/100))
            )

        else:
            if self.unit_price < 0:
                raise ValidationError('Unit Price must be positive')
            else:
                self.total = self.quantity_requested * self.unit_price
            self.quantity_requested -= self.quantity_received
            super(PurchaseLine, self).save(*args, **kwargs)
        try:
            self.quantity_requested -= self.quantity_received
            super(PurchaseLine,self).save(*args, **kwargs)
        except ValidationError as e:
            raise e

    def __str__(self) -> str:
        return f'{self.number}'

@receiver(post_save, sender=PurchaseLine)
def update_lpo_total(sender, instance, created, **kwargs):
    if created:
        lpo_header = instance.number
        total_amount = lpo_header.lines.filter(number__total=0).aggregate(total=Sum('total'))['total']
        lpo_header.total = total_amount or 0
        lpo_header.save()

class PurchaseCreditMemoHeader(models.Model):
    number = PurchaseCreditMemo(primary_key=True, editable=False)
    vendor = models.ForeignKey(PurchaseHeader, on_delete=models.PROTECT, related_name='memo', related_query_name='memo')
    date = models.DateField(auto_now=True)
    amount = models.PositiveBigIntegerField()
    created_by = models.ForeignKey('auth.User', blank=True, null=True, default=None, on_delete=models.PROTECT, related_name='purchase_memo', related_query_name='purchase_memo',editable=False)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(PurchaseHeader, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self.number}'
    def get_absolute_url(self):
        return reverse('inventory:purchasememo-detail', args=[str(self.number)])
    class Meta:
        ordering = ["number"]
        verbose_name_plural = "Purchase Credit Memos"

class PurchaseCreditMemoLine(models.Model):
    number = models.ForeignKey(PurchaseCreditMemoHeader, on_delete=models.PROTECT, related_name='lines', related_query_name='lines')
    item = models.CharField(max_length=100)
    purchase_line = models.ForeignKey(PurchaseLine, on_delete=models.PROTECT, related_name='purchase_line', related_query_name='purchase_line')
    batch = models.CharField(max_length=100)
    unit_price = models.PositiveIntegerField(editable=False)
    quantity = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    item_entry = models.ForeignKey('ItemEntry', on_delete=models.PROTECT, related_name='purchase_return', related_query_name='purchase_return')

    def __str__(self) -> str:
        return f'{self.number}'
    
    def save(self, *args, **kwargs):
        if not self.unit_price:
            purchase_line = self.purchase_line
            if purchase_line:
                self.item = purchase_line.item
                self.batch = purchase_line.batch
                self.unit_price = purchase_line.unit_price
                if self.quantity > purchase_line.quantity_received:
                    raise ValidationError(f'You cannot returned more({self.quantity}) than delivered({purchase_line.quantity_received})')
            item_entry = self.item_entry
            if item_entry:
                item_entry.quantity -= self.quantity
                item_entry.save()
        self.total = self.unit_price * self.quantity
        super(PurchaseCreditMemoLine, self).save(*args, **kwargs)

@receiver(post_save, sender=PurchaseCreditMemoLine)
def update_memo_total(sender, instance, created, **kwargs):
    if created:
        purchase_memo = instance.number
        total_amount = purchase_memo.line.aggregate(total=Sum('total'))['total']
        purchase_memo.amount = total_amount or 0
        purchase_memo.save()


class ItemEntry(models.Model):
    entry_date = models.DateField(auto_now_add=True, editable=False)
    purchase_doc_no = models.ForeignKey(PurchaseLine, on_delete=models.PROTECT, related_name='item_entry', related_query_name='item_entry', null=True, verbose_name='Purchase Document Number')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='grn', related_query_name='grn')
    batch = models.CharField('Batch Number', max_length=200, null=True)
    quantity = models.IntegerField()
    expiry_date = models.DateField('Expiry Date', default=datetime.date.today)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    sale = models.DecimalField(decimal_places=2, max_digits=10)
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
        if not self.expiry_date:
            self.expiry_date = datetime.date.today()
        self.expiry_status = self.is_expired
        #self.sale = self.cost * 1.4
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
        return reverse('inventory:invoice-detail', args=[str(self.number)])
    class Meta:
        verbose_name_plural = 'Sales Invoices'
        ordering = ["number"]

class SalesLines(models.Model):
    number = models.ForeignKey(SalesHeader, on_delete=models.CASCADE, related_name='lines', related_query_name='lines')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='invoices', related_query_name='invoices')
    batch = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField()
    lpo = models.ForeignKey(ItemEntry, on_delete=models.PROTECT, related_name='sales', related_query_name='sales',  null=True)
    unit_price = models.DecimalField(editable=False, decimal_places=2, max_digits=10)
    total = models.DecimalField(editable=False, decimal_places=2, max_digits=10)
    discount = models.DecimalField(validators=[MaxValueValidator(100)], default=0, help_text="Allowed Precentage Discount", max_digits=6, decimal_places=2)

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

class SalesCreditMemoHeader(models.Model):
    number = SalesCreditMemo(primary_key=True, editable=False)
    customer = models.CharField(max_length=200)
    date = models.DateField(auto_now=True) # put date logic (should not be earlier than invoice date but can equal invice date)
    invoice_no = models.ForeignKey(SalesLines, on_delete=models.PROTECT, related_name='credit_memo', related_query_name='credit_memo')
    amount = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey('auth.User', blank=True, null=True, default=None, on_delete=models.PROTECT, related_name='memo', related_query_name='memo',editable=False)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        #self.modified_by = user
        super(SalesCreditMemoHeader, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return f'{self.number}'
    
    def get_absolute_url(self):
        return reverse('inventory:salesmemo-detail', args=[str(self.number)])
    
    class Meta:
        ordering = ["number"]
        verbose_name_plural = 'Sales Credit Memos'

class SalesCreditMemoLine(models.Model):
    number = models.ForeignKey(SalesCreditMemoHeader, on_delete=models.PROTECT, related_name='lines', related_query_name='lines')
    item = models.CharField(help_text='Item to return', max_length=100)
    sales_line = models.ForeignKey(SalesLines, on_delete=models.PROTECT, related_name='sales_line', related_query_name='sales_line')
    batch = models.CharField(help_text='Batch number to return', max_length=100)
    unit_price = models.PositiveIntegerField(editable=False)
    quantity = models.PositiveIntegerField()
    total = models.IntegerField(editable=False)
    item_entry = models.ForeignKey(ItemEntry, on_delete=models.PROTECT, related_name='sales_return', related_query_name='sales_return')


    def save(self, *args, **kwargs):
        if not self.unit_price:
            invoice_line = self.sales_line
            if invoice_line:
                self.item = invoice_line.item 
                self.batch = invoice_line.batch 
                self.unit_price = invoice_line.unit_price 
                if self.quantity > invoice_line.quantity:
                    raise ValidationError(f'You can return more({self.quantity}) than issued({invoice_line.quantity})')
            item_entry = self.item_entry
            if item_entry:
                item_entry.quantity += self.quantity
                item_entry.save()
        self.total = self.unit_price * self.quantity
        super(SalesCreditMemoLine,self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self.number}'
@receiver(post_save, sender=SalesCreditMemoLine)
def update_memo_total(sender, instance, created, **kwargs):
    if created:
        sales_memo = instance.number
        total_amount = sales_memo.line.aggregate(total=Sum('total'))['total']
        sales_memo.amount = total_amount or 0
        sales_memo.save()

class ApprovalEntry(models.Model):
    requester = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.PROTECT, related_name='requestor', related_query_name='requestor')
    document_number = models.ForeignKey(PurchaseHeader, on_delete=models.PROTECT, related_name='approval', related_query_name='approval')
    details = models.CharField(max_length=200)
    approval_status = ((0,'Open'), (1,'Pending Approval'), (2,'Approved'), (3,'Cancelled Approval'))
    status = models.CharField(max_length=20, choices=approval_status)
    approver = models.ForeignKey('auth.User', on_delete=models.PROTECT, blank=True, null=True, related_name='approver', related_query_name='approver')
    amount = models.ForeignKey(PurchaseHeader, on_delete=models.PROTECT, related_name='approval_amount', related_query_name='approval_amount')
    request_date = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', blank=True, null=True, default=None, on_delete=models.PROTECT, related_name='modifier', related_query_name='modifier',editable=False)
    due_date = models.DateField(default=timezone.now)
    overdue = models.BooleanField(default=False)
    reason = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return f'{self.requester}-{self.document_number}: {self.details}'
    @property
    def is_overdue(self):
        return datetime.today - self.request_date < 5
    def save(self, *args, **kwargs):
        self.overdue = self.is_overdue
        self.details = "Amount: " + self.amount + "LPO Number: " + self.document_number
        super(ApprovalEntry, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('inventory:approval-detail', args=[str(self.id)])
    
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Approval Entries"

class ApprovalSetup(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='user', related_query_name='user')
    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approver_id', related_query_name='approver_id')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='modifier_id', related_query_name='modifier_id', editable=False)

    class Meta:
        verbose_name_plural = 'Approvals Setup'
    def __str__(self) -> str:
        return f"User:{self.user}   Approver:{self.approver}"
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.modified_by = user
        #self.modified_by = user
        super(ApprovalSetup, self).save(*args, **kwargs)
# @receiver(post_save, sender=User)
# def create_user_approval(sender, instance, created, **kwargs):
#     if created:
#         ApprovalSetup.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null= True)
    designation = models.CharField(max_length=100, null= True)
    mobile_number = models.CharField(max_length=20, null=True)
    profile_image = models.ImageField(default='profile.png',upload_to='profiles/')
    profile_summary = models.TextField(max_length=300, null= True)
    city = models.CharField(max_length=100, null= True)
    state = models.CharField(max_length=100, null= True)
    country = models.CharField(max_length=100, null= True)

    def __str__(self) -> str:
        return f"{self.full_name}'s profile"
    def save(self, *args, **kwargs):
        super().save()
        #super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.profile_image.path)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    
        





