# Generated by Django 2.0.5 on 2018-05-14 14:34

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myimpact', '0012_zoningdistrict'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zoningdistrict',
            name='the_geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326),
        ),
    ]
