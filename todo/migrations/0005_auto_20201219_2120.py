# Generated by Django 3.1.3 on 2020-12-19 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_task_ingredient_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='ingredient_type',
            new_name='ingredient_category',
        ),
    ]
