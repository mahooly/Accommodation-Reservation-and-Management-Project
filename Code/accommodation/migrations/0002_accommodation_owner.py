# Generated by Django 2.2.1 on 2019-06-07 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accommodation', '0001_initial'),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accommodation',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='registration.Host'),
        ),
    ]
