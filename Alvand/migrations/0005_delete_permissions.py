# Generated by Django 5.1.6 on 2025-02-26 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Alvand', '0004_remove_users_lastpasswordreset_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Permissions',
        ),
    ]
