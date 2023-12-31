# Generated by Django 4.2.2 on 2023-10-29 14:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0072_alter_approvalentry_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="approvalentry",
            name="status",
            field=models.CharField(
                choices=[
                    (0, "Open"),
                    (1, "Pending Approval"),
                    (2, "Approved"),
                    (3, "Cancelled Approval"),
                ],
                default=1,
                max_length=20,
            ),
        ),
    ]
