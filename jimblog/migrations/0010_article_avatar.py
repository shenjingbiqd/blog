# Generated by Django 3.1.5 on 2021-02-23 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jimblog', '0009_auto_20210221_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='post/%Y%m%d/'),
        ),
    ]
