# Generated by Django 4.2.2 on 2023-07-08 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_remove_saleslines_batch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesheader',
            name='amount',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
