# Generated by Django 3.2 on 2021-04-20 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app', '0004_remove_task_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]