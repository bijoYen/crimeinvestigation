# Generated by Django 3.0.3 on 2021-01-21 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppCriminal', '0002_auto_20210121_1247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suspects_details',
            name='Password',
        ),
    ]
