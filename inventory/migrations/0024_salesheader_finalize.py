# Generated by Django 4.2.2 on 2023-07-08 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_alter_salesheader_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesheader',
            name='finalize',
            field=models.BooleanField(default=False),
        ),
    ]