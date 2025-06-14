# Generated by Django 5.1.6 on 2025-04-10 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alvand', '0030_device_cabletype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='cableType',
        ),
        migrations.AddField(
            model_name='device',
            name='cable_type',
            field=models.CharField(blank=True, choices=[('rs-232c', 'RS-232C'), ('ethernet', 'ETHERNET')], null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='device',
            field=models.CharField(choices=[('KX-TA308', 'KX-TA308'), ('KX-TES824', 'KX-TES824'), ('KX-TEM824', 'KX-TEM824'), ('KX-TDA30', 'KX-TDA30'), ('KX-TDA100', 'KX-TDA100'), ('KX-TDA100D', 'KX-TDA100D'), ('KX-TDA100DBA', 'KX-TDA100DBA'), ('KX-TDA200', 'KX-TDA200'), ('KX-TDA600', 'KX-TDA600'), ('KX-TDE100', 'KX-TDE100'), ('KX-TDE200', 'KX-TDE200'), ('KX-TDE600', 'KX-TDE600'), ('KX-NS300', 'KX-NS300'), ('KX-NS500', 'KX-NS500'), ('KX-NS700', 'KX-NS700'), ('KX-NS1000', 'KX-NS1000'), ('KX-HTS32', 'KX-HTS32'), ('KX-HTS824', 'KX-HTS824')], max_length=191),
        ),
        migrations.AlterField(
            model_name='lices',
            name='version',
            field=models.CharField(choices=[('alvand', 'الوند'), ('binalud', 'بینالود')], max_length=50),
        ),
    ]
