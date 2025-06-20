# Generated by Django 5.1.6 on 2025-02-20 13:15

import django.contrib.postgres.fields
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Connections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=11)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Costs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hamrahaval', models.BigIntegerField()),
                ('irancell', models.BigIntegerField()),
                ('rightel', models.BigIntegerField()),
                ('provincial', models.BigIntegerField()),
                ('international', models.BigIntegerField()),
                ('outofprovincial', models.BigIntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=4, unique=True)),
                ('title', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stopbits', models.FloatField(blank=True, null=True)),
                ('baudrate', models.BigIntegerField(blank=True, null=True)),
                ('parity', models.TextField(blank=True, null=True)),
                ('databits', models.IntegerField(blank=True, null=True)),
                ('flow', models.TextField(blank=True, null=True)),
                ('smdrip', models.TextField(blank=True, null=True)),
                ('smdrport', models.IntegerField(blank=True, null=True)),
                ('smdrpassword', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Errors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('errorcodenum', models.BigIntegerField(unique=True)),
                ('errormessage', models.TextField(blank=True, null=True)),
                ('probablecause', models.TextField(blank=True, null=True)),
                ('solution', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('errorcode', models.BigIntegerField()),
                ('label', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Records',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='تاریخ:')),
                ('hour', models.TimeField(verbose_name='ساعت:')),
                ('extension', models.CharField(blank=True, max_length=200, null=True)),
                ('urbanline', models.CharField(blank=True, max_length=200, null=True)),
                ('contactnumber', models.CharField(blank=True, max_length=200, null=True)),
                ('calltype', models.CharField(max_length=200)),
                ('durationtime', models.CharField(blank=True, max_length=200, null=True)),
                ('internal', models.BigIntegerField(blank=True, null=True)),
                ('beepsnumber', models.CharField(blank=True, max_length=200, null=True)),
                ('transferring', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), blank=True, null=True, size=None)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Telephons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.BigIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=200, unique=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(blank=True, null=True)),
                ('pename', models.CharField(max_length=200)),
                ('enname', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'unique_together': {('pename', 'enname')},
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('online', models.IntegerField(default=True)),
                ('extension', models.BigIntegerField()),
                ('internal', models.BigIntegerField(default=0)),
                ('usersextension', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), blank=True, null=True, size=None, verbose_name='دسترسی های داخلی:')),
                ('name', models.CharField(max_length=191, verbose_name='نام:')),
                ('username', models.CharField(max_length=191, unique=True, verbose_name='نام کاربری:')),
                ('lastname', models.CharField(max_length=191, verbose_name='نام خانوادگی:')),
                ('groupname', models.CharField(max_length=191)),
                ('picurl', models.CharField(default='avatar.png', max_length=191)),
                ('email', models.CharField(max_length=191, unique=True)),
                ('email_verified_at', models.DateTimeField(blank=True, null=True)),
                ('password', models.CharField(max_length=191)),
                ('remember_token', models.CharField(blank=True, max_length=191, null=True)),
                ('lastpasswordreset', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Alvand.groups')),
            ],
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perm_email', models.BooleanField(blank=True, null=True)),
                ('can_view', models.BooleanField(default=False)),
                ('can_write', models.BooleanField(default=False)),
                ('can_delete', models.BooleanField(default=False)),
                ('can_modify', models.BooleanField(default=False)),
                ('exts_label', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), blank=True, null=True, size=None)),
                ('errorsreport', models.BooleanField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to='Alvand.users')),
            ],
        ),
        migrations.CreateModel(
            name='Infos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthdate', models.TextField(blank=True, null=True, verbose_name='تاریخ تولد:')),
                ('phonenumber', models.CharField(blank=True, max_length=191, null=True, verbose_name='شماره همراه:')),
                ('telephone', models.CharField(blank=True, max_length=191, null=True, verbose_name='تلفن:')),
                ('province', models.CharField(blank=True, max_length=191, null=True, verbose_name='استان:')),
                ('city', models.CharField(blank=True, max_length=191, null=True, verbose_name='شهر:')),
                ('address', models.CharField(blank=True, max_length=191, null=True, verbose_name='آدرس:')),
                ('gender', models.IntegerField(blank=True, choices=[('0', 'مرد'), ('1', 'زن'), ('2', 'نامعلوم')], null=True, verbose_name='جنسیت:')),
                ('military', models.CharField(blank=True, choices=[('0', 'مشمول'), ('1', 'پایان خدمت'), ('2', 'معافیت پزشکی'), ('3', 'معافیت تحصیلی'), ('4', 'معافیت سایر')], max_length=191, null=True, verbose_name='وضعیت نظام وظیفه:')),
                ('maritalstatus', models.CharField(blank=True, choices=[('0', 'متاهل'), ('1', 'مجرد')], max_length=191, null=True, verbose_name='وضعیت تاهل:')),
                ('educationdegree', models.CharField(blank=True, choices=[('0', 'زیر دیپلم'), ('1', 'دیپلم'), ('2', 'فوق دیپلم'), ('3', 'لیسانس '), ('4', 'فوق لیسانس'), ('5', 'دکترا'), ('6', 'فوق دکترا')], max_length=191, null=True, verbose_name='مدرک')),
                ('educationfield', models.CharField(blank=True, max_length=191, null=True, verbose_name='زمینه مدرک:')),
                ('cardnumber', models.CharField(blank=True, max_length=191, null=True, verbose_name='شماره کارت:')),
                ('accountnumber', models.CharField(blank=True, max_length=191, null=True, verbose_name='شماره حساب:')),
                ('accountnumbershaba', models.CharField(blank=True, max_length=191, null=True, verbose_name='شماره حساب:')),
                ('macaddress', models.CharField(blank=True, default=None, max_length=191, null=True, verbose_name='مک آدرس:')),
                ('nationalcode', models.BigIntegerField(blank=True, null=True, verbose_name='کد ملی:')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to='Alvand.users')),
            ],
        ),
        migrations.CreateModel(
            name='Extensionsgroups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exts', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), blank=True, null=True, size=None)),
                ('label', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('modifyby', models.ForeignKey(db_column='modifyby', on_delete=django.db.models.deletion.DO_NOTHING, to='Alvand.users')),
            ],
        ),
        migrations.CreateModel(
            name='Emailsending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailtosend', models.TextField(unique=True)),
                ('collectionusername', models.TextField()),
                ('collectionpassword', models.TextField()),
                ('lines', models.IntegerField(blank=True, null=True)),
                ('errors', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), blank=True, null=True, size=None)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('byadmin', models.ForeignKey(db_column='byadmin', on_delete=django.db.models.deletion.CASCADE, to='Alvand.users')),
            ],
        ),
        migrations.CreateModel(
            name='Verifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=0)),
                ('code', models.BigIntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.DO_NOTHING, to='Alvand.users')),
            ],
        ),
    ]
