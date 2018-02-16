# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-02 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NLP4CCB', '0007_auto_20170714_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstat',
            name='concreteness_index',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pass',
            name='type',
            field=models.CharField(choices=[('hyponyms', 'hyponyms'), ('meronyms', 'meronyms'), ('antonyms', 'antonyms'), ('synonyms', 'synonyms'), ('concreteness', 'concreteness')], max_length=50),
        ),
    ]
