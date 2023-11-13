# Generated by Django 4.2.2 on 2023-10-23 16:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0069_alter_purchaseline_markup"),
    ]

    operations = [
        migrations.AlterField(
            model_name="saleslines",
            name="discount",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                help_text="Allowed Precentage Discount",
                max_digits=6,
                validators=[django.core.validators.MaxValueValidator(100)],
            ),
        ),
    ]