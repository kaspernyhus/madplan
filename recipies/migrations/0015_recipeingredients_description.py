# Generated by Django 3.1.3 on 2020-12-20 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0014_auto_20201215_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeingredients',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
