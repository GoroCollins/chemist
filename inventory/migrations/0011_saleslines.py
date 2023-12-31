# Generated by Django 4.2.2 on 2023-07-03 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_alter_purchaseheader_created_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesLines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('unit_price', models.IntegerField()),
                ('total', models.FloatField()),
                ('discount', models.IntegerField(default=0, verbose_name='Percentage Discount')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invoices', related_query_name='invoices', to='inventory.item')),
                ('lpo', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='sales', related_query_name='sales', to='inventory.itementry')),
                ('number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', related_query_name='lines', to='inventory.salesheader')),
            ],
        ),
    ]
