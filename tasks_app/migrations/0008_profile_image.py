# Generated by Django 3.2 on 2021-04-23 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app', '0007_auto_20210421_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
