# Generated by Django 4.2.2 on 2023-07-21 18:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0029_alter_approvalentry_options_alter_item_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseline',
            name='markup',
            field=models.PositiveSmallIntegerField(default=40, help_text='Percentage Markup', validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='itementry',
            name='cost',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='itementry',
            name='sale',
            field=models.FloatField(),
        ),
    ]
