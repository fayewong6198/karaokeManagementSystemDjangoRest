# Generated by Django 3.0.6 on 2020-05-14 16:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkInDate', models.DateTimeField(default=datetime.datetime.now)),
                ('checkOutDate', models.DateTimeField(default=datetime.datetime.now)),
                ('totalHourSpend', models.DecimalField(decimal_places=2, max_digits=15)),
                ('status', models.CharField(choices=[('checkedIn', 'CHECKED IN'), ('checkedOut', 'CHECKED OUT')], default='checkedIn', max_length=31)),
                ('total', models.DecimalField(decimal_places=2, max_digits=20)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payments', to='rooms.Room')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=255, unique=True)),
                ('productName', models.CharField(max_length=255)),
                ('price', models.IntegerField(default=0)),
                ('discount', models.IntegerField(default=0)),
                ('description', models.TextField()),
                ('stock', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('catetory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='rooms.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductUsed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='rooms.Payment')),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='rooms.Product')),
            ],
        ),
    ]
