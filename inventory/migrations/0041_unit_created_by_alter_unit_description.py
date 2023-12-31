# Generated by Django 4.2.2 on 2023-07-26 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0040_purchasecreditmemoheader_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='units', related_query_name='units', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='unit',
            name='description',
            field=models.CharField(max_length=200, verbose_name='Unit of Measure'),
        ),
    ]
