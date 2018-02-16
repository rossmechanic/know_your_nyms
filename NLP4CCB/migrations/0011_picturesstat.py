# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-30 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NLP4CCB', '0010_auto_20171127_0123'),
    ]

    operations = [
        migrations.CreateModel(
            name='PicturesStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50)),
                ('index', models.IntegerField(default=0)),
                ('sem_rel', models.CharField(max_length=50)),
                ('avg_score', models.FloatField(default=0.0)),
                ('total_score', models.FloatField(default=0.0)),
                ('rounds_played', models.IntegerField(default=0)),
            ],
        ),
    ]
