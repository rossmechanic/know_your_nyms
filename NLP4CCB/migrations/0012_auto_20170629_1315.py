# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NLP4CCB', '0011_auto_20170626_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmationStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sem_rel', models.CharField(max_length=50)),
                ('base_word', models.CharField(max_length=50)),
                ('input_word', models.CharField(max_length=50)),
                ('times_confirmed', models.IntegerField(default=0)),
                ('times_rejected', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='relation',
            name='times_confirmed',
        ),
        migrations.RemoveField(
            model_name='relation',
            name='times_rejected',
        ),
        migrations.RemoveField(
            model_name='relation',
            name='times_suggested',
        ),
    ]
