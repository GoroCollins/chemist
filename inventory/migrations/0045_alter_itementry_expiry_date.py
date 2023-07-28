# Generated by Django 4.2.2 on 2023-07-28 18:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0044_alter_itementry_expiry_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itementry',
            name='expiry_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Expiry Date'),
        ),
    ]
