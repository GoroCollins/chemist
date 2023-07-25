# Generated by Django 4.2.2 on 2023-07-23 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0035_delete_salescreditmemoline'),
    ]

    operations = [
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
                ('sales_line', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.saleslines')),
            ],
        ),
    ]