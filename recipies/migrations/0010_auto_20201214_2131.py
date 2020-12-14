# Generated by Django 3.1.3 on 2020-12-14 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0009_recipies_photo_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='recipies',
            name='tags',
            field=models.ManyToManyField(to='recipies.RecipeTags'),
        ),
    ]
