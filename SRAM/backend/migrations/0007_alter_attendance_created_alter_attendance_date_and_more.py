# Generated by Django 4.2.1 on 2023-07-05 20:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_attendance_created_alter_attendance_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 538338)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 538339)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 538338)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 536338)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 536338)),
        ),
        migrations.AlterField(
            model_name='batchcoursefaculty',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 537339)),
        ),
        migrations.AlterField(
            model_name='batchcoursefaculty',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 537339)),
        ),
        migrations.AlterField(
            model_name='codes',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 537339)),
        ),
        migrations.AlterField(
            model_name='codes',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 537339)),
        ),
        migrations.AlterField(
            model_name='course',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 536338)),
        ),
        migrations.AlterField(
            model_name='course',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 536338)),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 535341)),
        ),
        migrations.AlterField(
            model_name='facultycodestatus',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 538338)),
        ),
        migrations.AlterField(
            model_name='facultycodestatus',
            name='lastActivated',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 538338), verbose_name='LastActivated'),
        ),
        migrations.AlterField(
            model_name='facultycodestatus',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 538338)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 534347)),
        ),
        migrations.AlterField(
            model_name='qrcode',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 538338)),
        ),
        migrations.AlterField(
            model_name='qrcode',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 538338)),
        ),
        migrations.AlterField(
            model_name='student',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 533340)),
        ),
        migrations.AlterField(
            model_name='student',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 534347)),
        ),
        migrations.AlterField(
            model_name='verifiedemails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 6, 2, 25, 28, 535341)),
        ),
    ]
