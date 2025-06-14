# Generated by Django 5.1.6 on 2025-02-24 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alvand', '0003_alter_users_email_alter_users_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='lastpasswordreset',
        ),
        migrations.RemoveField(
            model_name='users',
            name='remember_token',
        ),
        migrations.AlterField(
            model_name='permissions',
            name='can_delete',
            field=models.BooleanField(default=False, verbose_name='مجوز حذف کردن'),
        ),
        migrations.AlterField(
            model_name='permissions',
            name='can_modify',
            field=models.BooleanField(default=False, verbose_name='مجوز ویرایش کردن'),
        ),
        migrations.AlterField(
            model_name='permissions',
            name='can_view',
            field=models.BooleanField(default=False, verbose_name='مجوز دیدن'),
        ),
        migrations.AlterField(
            model_name='permissions',
            name='can_write',
            field=models.BooleanField(default=False, verbose_name='مجوز ایجاد کردن'),
        ),
    ]
