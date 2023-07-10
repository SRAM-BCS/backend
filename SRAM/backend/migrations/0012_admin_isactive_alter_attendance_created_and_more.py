# Generated by Django 4.2.1 on 2023-07-09 21:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_alter_attendance_created_alter_attendance_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 804113)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 804113)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 804113)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 802126)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 802126)),
        ),
        migrations.AlterField(
            model_name='batchcoursefaculty',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 804113)),
        ),
        migrations.AlterField(
            model_name='batchcoursefaculty',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 804113)),
        ),
        migrations.AlterField(
            model_name='codes',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 803114)),
        ),
        migrations.AlterField(
            model_name='codes',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 803114)),
        ),
        migrations.AlterField(
            model_name='course',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 803114)),
        ),
        migrations.AlterField(
            model_name='course',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 803114)),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 801117)),
        ),
        migrations.AlterField(
            model_name='facultycodestatus',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 805138)),
        ),
        migrations.AlterField(
            model_name='facultycodestatus',
            name='lastActivated',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 805138), verbose_name='LastActivated'),
        ),
        migrations.AlterField(
            model_name='facultycodestatus',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 805138)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 801117)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 10, 3, 7, 27, 801117)),
        ),
        migrations.AlterField(
            model_name='qrcodetable',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 805138)),
        ),
        migrations.AlterField(
            model_name='qrcodetable',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 805138)),
        ),
        migrations.AlterField(
            model_name='student',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 800119)),
        ),
        migrations.AlterField(
            model_name='student',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 800119)),
        ),
        migrations.AlterField(
            model_name='verifiedemails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 10, 3, 4, 27, 801117)),
        ),
    ]
