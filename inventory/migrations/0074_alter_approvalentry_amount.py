# Generated by Django 4.2.2 on 2023-10-31 02:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0073_alter_approvalentry_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="approvalentry",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
