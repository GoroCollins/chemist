# Generated by Django 4.2.2 on 2023-07-29 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0046_alter_purchaseline_unit_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itementry',
            name='batch',
            field=models.CharField(max_length=200, null=True, verbose_name='Batch Number'),
        ),
    ]
