# Generated by Django 5.1.6 on 2025-04-10 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Alvand', '0031_remove_device_cabletype_device_cable_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='cable_type',
            new_name='cableType',
        ),
    ]
