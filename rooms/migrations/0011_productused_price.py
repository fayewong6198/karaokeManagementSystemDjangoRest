# Generated by Django 3.0.6 on 2020-06-17 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0010_auto_20200529_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='productused',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
