# Generated by Django 4.2.2 on 2023-09-10 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0057_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(null=True, upload_to='profiles/'),
        ),
    ]
