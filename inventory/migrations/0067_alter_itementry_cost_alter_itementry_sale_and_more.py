# Generated by Django 4.2.2 on 2023-10-22 17:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0066_alter_itementry_cost_alter_itementry_sale_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itementry",
            name="cost",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="itementry",
            name="sale",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="purchaseline",
            name="unit_price",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="Unit Price"
            ),
        ),
        migrations.AlterField(
            model_name="saleslines",
            name="total",
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name="saleslines",
            name="unit_price",
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10),
        ),
    ]