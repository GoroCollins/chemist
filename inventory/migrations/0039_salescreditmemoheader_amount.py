# Generated by Django 4.2.2 on 2023-07-23 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0038_alter_salescreditmemoline_sales_line'),
    ]

    operations = [
        migrations.AddField(
            model_name='salescreditmemoheader',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
