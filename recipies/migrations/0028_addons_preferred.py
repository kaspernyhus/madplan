# Generated by Django 3.1.3 on 2021-02-04 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0027_addons_qty_multiplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='addons',
            name='preferred',
            field=models.ManyToManyField(to='recipies.Recipies'),
        ),
    ]