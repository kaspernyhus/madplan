# Generated by Django 3.1.3 on 2021-01-17 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0016_auto_20210117_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipies',
            name='prep_time',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
