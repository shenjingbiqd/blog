# Generated by Django 3.1.5 on 2021-02-21 14:52

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('jimblog', '0008_auto_20210220_1131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='topic',
        ),
        migrations.AddField(
            model_name='article',
            name='topic',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
