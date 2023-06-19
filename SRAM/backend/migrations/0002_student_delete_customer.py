# Generated by Django 4.2.1 on 2023-06-02 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
                ('email', models.EmailField(max_length=254)),
                ('roll', models.CharField(max_length=240, verbose_name='RollNumber')),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]