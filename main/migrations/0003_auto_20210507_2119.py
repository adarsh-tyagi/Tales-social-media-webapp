# Generated by Django 3.1.5 on 2021-05-07 15:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210507_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 7, 21, 19, 43, 685359)),
        ),
    ]