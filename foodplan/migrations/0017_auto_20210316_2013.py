# Generated by Django 3.1.3 on 2021-03-16 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0016_auto_20210125_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodplanrecipies',
            name='quantity',
            field=models.FloatField(default=1.0),
        ),
    ]
