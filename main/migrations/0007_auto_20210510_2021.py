# Generated by Django 3.1.5 on 2021-05-10 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210507_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 10, 20, 21, 16, 164284)),
        ),
    ]
