# Generated by Django 3.2 on 2021-04-23 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app', '0012_auto_20210423_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='day',
            name='user',
        ),
    ]
