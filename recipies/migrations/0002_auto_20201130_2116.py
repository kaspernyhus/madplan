# Generated by Django 3.1.3 on 2020-11-30 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredients',
            name='measurement_unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='recipies.measurementunits'),
        ),
    ]
