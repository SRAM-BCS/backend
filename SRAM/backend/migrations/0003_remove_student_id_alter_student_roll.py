# Generated by Django 4.2.1 on 2023-06-02 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_student_delete_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='id',
        ),
        migrations.AlterField(
            model_name='student',
            name='roll',
            field=models.CharField(max_length=240, primary_key=True, serialize=False, verbose_name='RollNumber'),
        ),
    ]
