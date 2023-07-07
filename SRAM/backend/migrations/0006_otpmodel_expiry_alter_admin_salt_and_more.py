# Generated by Django 4.2.1 on 2023-07-07 14:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_merge_20230707_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpmodel',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 7, 20, 20, 4, 130495)),
        ),
        migrations.AlterField(
            model_name='admin',
            name='salt',
            field=models.CharField(default='Nothing', verbose_name='Salt'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 132505)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 132505)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 132505)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 131505)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 131505)),
        ),
        migrations.AlterField(
            model_name='batchcoursefaculty',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 132505)),
        ),
        migrations.AlterField(
            model_name='batchcoursefaculty',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 132505)),
        ),
        migrations.AlterField(
            model_name='codes',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 132505)),
        ),
        migrations.AlterField(
            model_name='codes',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 132505)),
        ),
        migrations.AlterField(
            model_name='course',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 131505)),
        ),
        migrations.AlterField(
            model_name='course',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 131505)),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 131505)),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='salt',
            field=models.CharField(default='Nothing', verbose_name='Salt'),
        ),
        migrations.AlterField(
            model_name='facultycodestatus',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 133508)),
        ),
        migrations.AlterField(
            model_name='facultycodestatus',
            name='lastActivated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 133508), verbose_name='LastActivated'),
        ),
        migrations.AlterField(
            model_name='facultycodestatus',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 133508)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 130495)),
        ),
        migrations.AlterField(
            model_name='qrcodetable',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 133508)),
        ),
        migrations.AlterField(
            model_name='qrcodetable',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 133508)),
        ),
        migrations.AlterField(
            model_name='student',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 130495)),
        ),
        migrations.AlterField(
            model_name='student',
            name='salt',
            field=models.CharField(default='Nothing', verbose_name='Salt'),
        ),
        migrations.AlterField(
            model_name='student',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 130495)),
        ),
        migrations.AlterField(
            model_name='verifiedemails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 7, 20, 17, 4, 131505)),
        ),
    ]