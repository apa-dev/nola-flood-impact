# Generated by Django 2.0.5 on 2018-05-14 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myimpact', '0008_buildingfootprint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingfootprint',
            name='geopin',
            field=models.FloatField(),
        ),
    ]
