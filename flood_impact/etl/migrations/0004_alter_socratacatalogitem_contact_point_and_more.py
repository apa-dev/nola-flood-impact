# Generated by Django 5.1.3 on 2024-11-18 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etl', '0003_auto_20180511_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socratacatalogitem',
            name='contact_point',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='socratacatalogitem',
            name='distribution',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='socratacatalogitem',
            name='publisher',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
