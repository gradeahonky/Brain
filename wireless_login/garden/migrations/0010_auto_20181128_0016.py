# Generated by Django 2.1.3 on 2018-11-28 00:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0009_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlet',
            name='uvb_end_date',
            field=models.DateField(default=datetime.date(2019, 2, 26)),
        ),
    ]
