# Generated by Django 5.1.6 on 2025-03-04 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alvand', '0015_device_number_of_lines_alter_device_baudrate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costs',
            name='hamrahaval',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='costs',
            name='international',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='costs',
            name='irancell',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='costs',
            name='outofprovincial',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='costs',
            name='provincial',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='costs',
            name='rightel',
            field=models.FloatField(),
        ),
    ]
