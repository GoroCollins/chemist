# Generated by Django 4.2.2 on 2023-07-08 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_saleslines_batch_alter_saleslines_lpo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleslines',
            name='batch',
            field=models.CharField(max_length=100, null=True),
        ),
    ]