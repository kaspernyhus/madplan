# Generated by Django 3.1.3 on 2020-12-04 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0005_recipies_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredients',
            name='best_before',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]