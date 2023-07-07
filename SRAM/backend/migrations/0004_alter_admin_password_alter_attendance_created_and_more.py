# Generated by Django 4.2.1 on 2023-07-07 11:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_admin_salt_alter_attendance_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='password',
            field=models.CharField(blank=True, default='', max_length=240, null=True, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 450776)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 450776)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 450776)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 447776)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 447776)),
        ),
        migrations.AlterField(
            model_name='batchcoursefaculty',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 449774)),
        ),
        migrations.AlterField(
            model_name='batchcoursefaculty',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 449774)),
        ),
        migrations.AlterField(
            model_name='codes',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 448776)),
        ),
        migrations.AlterField(
            model_name='codes',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 448776)),
        ),
        migrations.AlterField(
            model_name='course',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 447776)),
        ),
        migrations.AlterField(
            model_name='course',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 447776)),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 445779)),
        ),
        migrations.AlterField(
            model_name='facultycodestatus',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 451775)),
        ),
        migrations.AlterField(
            model_name='facultycodestatus',
            name='lastActivated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 451775), verbose_name='LastActivated'),
        ),
        migrations.AlterField(
            model_name='facultycodestatus',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 451775)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 444766)),
        ),
        migrations.AlterField(
            model_name='qrcodetable',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 450776)),
        ),
        migrations.AlterField(
            model_name='qrcodetable',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 450776)),
        ),
        migrations.AlterField(
            model_name='student',
            name='created',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 442786)),
        ),
        migrations.AlterField(
            model_name='student',
            name='updated',
            field=models.DateField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 442786)),
        ),
        migrations.AlterField(
            model_name='verifiedemails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 7, 17, 4, 57, 445779)),
        ),
    ]
