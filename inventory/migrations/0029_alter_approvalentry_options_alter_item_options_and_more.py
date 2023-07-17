# Generated by Django 4.2.2 on 2023-07-17 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0028_alter_approvalentry_due_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='approvalentry',
            options={'ordering': ['id'], 'verbose_name_plural': 'Approval Entries'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['code'], 'verbose_name_plural': 'Items'},
        ),
        migrations.AlterModelOptions(
            name='purchaseheader',
            options={'ordering': ['number'], 'verbose_name_plural': 'Purchase Orders'},
        ),
        migrations.AlterModelOptions(
            name='salesheader',
            options={'ordering': ['number'], 'verbose_name_plural': 'Sales Invoices'},
        ),
        migrations.AlterModelOptions(
            name='vendor',
            options={'ordering': ['code'], 'verbose_name_plural': 'Vendors'},
        ),
    ]
