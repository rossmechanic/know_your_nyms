# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-01 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NLP4CCB', '0007_auto_20170601_1457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='completedstat',
            name='word_ind',
        ),
        migrations.RemoveField(
            model_name='userstat',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='wordstat',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='wordstat',
            name='std_dev',
        ),
        migrations.AddField(
            model_name='completedstat',
            name='base_word',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='completedstat',
            name='index',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='completedstat',
            name='sem_rel',
            field=models.CharField(default='synonyms', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wordstat',
            name='index',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wordstat',
            name='rounds_played',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wordstat',
            name='word',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
