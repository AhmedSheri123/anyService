# Generated by Django 4.2.16 on 2024-12-06 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_servicemodel_geo_lat_servicemodel_geo_lng'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='geo_lat',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='geo_lng',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
