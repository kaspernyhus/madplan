# Generated by Django 3.1.3 on 2021-01-30 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0024_auto_20210130_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipies',
            name='add_ons',
            field=models.BooleanField(default=0),
        ),
    ]