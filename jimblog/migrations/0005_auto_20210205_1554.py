# Generated by Django 3.1.5 on 2021-02-05 15:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jimblog', '0004_auto_20210205_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='article',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]