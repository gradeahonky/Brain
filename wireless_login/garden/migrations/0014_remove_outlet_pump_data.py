# Generated by Django 2.1.3 on 2018-12-01 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0013_auto_20181201_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outlet',
            name='pump_data',
        ),
    ]
