# Generated by Django 4.2.2 on 2023-07-23 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0032_alter_saleslines_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesCreditMemoHeader',
            fields=[
                ('number', inventory.models.SalesCreditMemo(editable=False, max_length=15, primary_key=True, serialize=False, unique=True)),
                ('customer', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='memo', related_query_name='memo', to=settings.AUTH_USER_MODEL)),
                ('invoice_no', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='credit_memo', related_query_name='credit_memo', to='inventory.salesheader')),
            ],
            options={
                'verbose_name_plural': 'Sales Credit Memos',
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='SalesCreditMemoLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(help_text='Item to return', max_length=100)),
                ('batch', models.CharField(help_text='Batch number to return', max_length=100)),
                ('unit_price', models.PositiveIntegerField(editable=False)),
                ('quantity', models.PositiveIntegerField()),
                ('total', models.IntegerField(editable=False)),
                ('item_entry', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='item_return', related_query_name='item_return', to='inventory.itementry')),
                ('number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='line', related_query_name='line', to='inventory.salescreditmemoheader')),
            ],
        ),
    ]
