# Generated by Django 5.1.6 on 2025-03-13 08:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alvand', '0023_delete_errorssent'),
    ]

    operations = [
        migrations.CreateModel(
            name='errorsSent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('success', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('fault', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Alvand.users')),
            ],
        ),
    ]
