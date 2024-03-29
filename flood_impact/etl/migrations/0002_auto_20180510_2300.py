# Generated by Django 2.0.5 on 2018-05-10 23:00

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socratacatalogitem',
            name='access_level',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='socratacatalogitem',
            name='contact_point',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='socratacatalogitem',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='socratacatalogitem',
            name='distribution',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='socratacatalogitem',
            name='issued',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='socratacatalogitem',
            name='landing_page',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='socratacatalogitem',
            name='modified',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='socratacatalogitem',
            name='publisher',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
