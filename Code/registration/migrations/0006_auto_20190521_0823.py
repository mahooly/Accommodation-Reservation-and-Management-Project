# Generated by Django 2.2.1 on 2019-05-21 08:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_auto_20190521_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birth_date',
            field=models.DateField(default=datetime.datetime(2019, 5, 21, 8, 23, 57, 620990)),
        ),
    ]
