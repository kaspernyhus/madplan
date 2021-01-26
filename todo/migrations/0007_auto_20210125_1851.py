# Generated by Django 3.1.3 on 2021-01-25 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_auto_20201220_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shoppinglist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('list_source', models.CharField(default=None, max_length=50)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='task',
            name='foodplan',
        ),
        migrations.AddField(
            model_name='task',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='todo.shoppinglist'),
        ),
    ]