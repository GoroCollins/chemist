# Generated by Django 4.2.2 on 2023-08-07 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0047_alter_itementry_batch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salescreditmemoline',
            name='number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lines', related_query_name='lines', to='inventory.salescreditmemoheader'),
        ),
    ]