# Generated by Django 3.1.3 on 2021-01-30 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0021_recipies_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipies',
            name='add_ons',
            field=models.BooleanField(default=0),
        ),
    ]
