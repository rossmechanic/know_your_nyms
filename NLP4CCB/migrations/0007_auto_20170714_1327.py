# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-14 17:27


import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("NLP4CCB", "0006_pass"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompletedStat",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sem_rel", models.CharField(max_length=50)),
                ("index", models.IntegerField(default=0)),
                ("base_word", models.CharField(max_length=50)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ConfirmationStat",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sem_rel", models.CharField(max_length=50)),
                ("base_word", models.CharField(max_length=50)),
                ("input_word", models.CharField(max_length=50)),
                ("times_confirmed", models.IntegerField(default=0)),
                ("times_rejected", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="WordStat",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("word", models.CharField(max_length=50)),
                ("index", models.IntegerField(default=0)),
                ("sem_rel", models.CharField(max_length=50)),
                ("avg_score", models.FloatField(default=0.0)),
                ("rounds_played", models.IntegerField(default=0)),
                ("retired", models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name="userstat",
            name="last_login",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
