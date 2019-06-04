# Generated by Django 2.2.1 on 2019-06-04 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('accommodation_type', models.CharField(choices=[('هتل', 'هتل'), ('اقامتگاه', 'اقامتگاه'), ('منزل شخصی', 'منزل شخصی')], max_length=20)),
                ('province', models.CharField(default='تهران', max_length=30)),
                ('city', models.CharField(default='تهران', max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('is_authenticated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_wifi', models.BooleanField(default=False)),
                ('has_tv', models.BooleanField(default=False)),
                ('has_warm_ac', models.BooleanField(default=False)),
                ('has_cool_ac', models.BooleanField(default=False)),
                ('has_parking', models.BooleanField(default=False)),
                ('has_kitchen', models.BooleanField(default=False)),
                ('has_utensils', models.BooleanField(default=False)),
                ('has_fridge', models.BooleanField(default=False)),
                ('has_oven', models.BooleanField(default=False)),
                ('has_bedsheets', models.BooleanField(default=False)),
                ('has_bathroom', models.BooleanField(default=False)),
                ('has_shower', models.BooleanField(default=False)),
                ('has_tub', models.BooleanField(default=False)),
                ('has_toilet', models.BooleanField(default=False)),
                ('has_hairdryer', models.BooleanField(default=False)),
                ('has_roomservice', models.BooleanField(default=False)),
                ('has_laundry', models.BooleanField(default=False)),
                ('has_elevator', models.BooleanField(default=False)),
                ('has_safe', models.BooleanField(default=False)),
                ('has_iron', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bed_type', models.CharField(choices=[('Single', 'تخت یک نفره'), ('Double', 'تخت دو نفره'), ('Twin', 'دو تخت یک نفره')], max_length=20)),
                ('number_of_guests', models.IntegerField()),
                ('how_many', models.IntegerField(default=1)),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodation.Accommodation')),
                ('amenity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='room', to='accommodation.Amenity')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='../media/house_pics/')),
                ('accommodation', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='accommodation.Accommodation')),
            ],
        ),
        migrations.AddField(
            model_name='accommodation',
            name='amenity',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='accommodation', to='accommodation.Amenity'),
        ),
        migrations.AddField(
            model_name='accommodation',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='registration.Host'),
        ),
    ]
