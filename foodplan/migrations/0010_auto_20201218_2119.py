# Generated by Django 3.1.3 on 2020-12-18 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0009_auto_20201218_1205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodplans',
            old_name='foodplan_id',
            new_name='foodplan',
        ),
    ]
