# Generated by Django 4.2.2 on 2023-07-08 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_alter_salesheader_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleslines',
            name='lpo',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sales', related_query_name='sales', to='inventory.itementry'),
        ),
    ]
