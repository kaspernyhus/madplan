# Generated by Django 3.1.3 on 2020-12-18 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0010_auto_20201218_2119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodplans',
            old_name='foodplan',
            new_name='foodplan_id',
        ),
    ]