# Generated by Django 3.1.3 on 2020-12-01 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0003_auto_20201130_2118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipetypes',
            old_name='type_name',
            new_name='name',
        ),
    ]