# Generated by Django 3.1.3 on 2020-12-04 21:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0004_auto_20201201_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipies',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]