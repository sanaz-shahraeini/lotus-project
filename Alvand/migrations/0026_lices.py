# Generated by Django 5.1.6 on 2025-03-25 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alvand', '0025_alter_errorssent_fault'),
    ]

    operations = [
        migrations.CreateModel(
            name='lices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lice', models.TextField(default=None, max_length=500)),
                ('active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
