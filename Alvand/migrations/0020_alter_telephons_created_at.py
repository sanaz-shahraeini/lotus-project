# Generated by Django 5.1.6 on 2025-03-06 08:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alvand', '0019_alter_permissions_errorsreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telephons',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
