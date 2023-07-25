# Generated by Django 4.2.2 on 2023-07-23 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0036_salescreditmemoline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salescreditmemoheader',
            name='invoice_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='credit_memo', related_query_name='credit_memo', to='inventory.saleslines'),
        ),
    ]