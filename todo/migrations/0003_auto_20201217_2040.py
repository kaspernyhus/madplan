# Generated by Django 3.1.3 on 2020-12-17 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_task_foodplan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='foodplan',
            field=models.IntegerField(default=1),
        ),
    ]
