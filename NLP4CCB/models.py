from __future__ import unicode_literals
from django import forms
from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.

class WordRelationshipForm(forms.Form):
	word = forms.CharField(
		max_length=100,
		widget=forms.TextInput()
	)
	submittime = forms.IntegerField()
	
class UserStat(models.Model):
	user = models.OneToOneField(User)
	rounds_played = models.IntegerField(default=0)
	total_score = models.FloatField(default=0.0)

	synonyms_index = models.IntegerField(default=0)
	antonyms_index = models.IntegerField(default=0)
	hyponyms_index = models.IntegerField(default=0)
	meronyms_index = models.IntegerField(default=0)
	concreteness_index = models.IntegerField(default=0)
	pictures_index = models.IntegerField(default=0)
	last_login = models.DateField(default=date.today)

class CompletedStat(models.Model):
	user = models.ForeignKey(User)
	sem_rel = models.CharField(max_length=50)
	index = models.IntegerField(default=0)
	base_word = models.CharField(max_length=50)

class WordStat(models.Model):
	word = models.CharField(max_length=50)
	index = models.IntegerField(default=0)
	sem_rel = models.CharField(max_length=50)
	avg_score = models.FloatField(default=0.0)
	rounds_played = models.IntegerField(default=0)
	retired = models.BooleanField(default=False)

class ConfirmationStat(models.Model):
	sem_rel = models.CharField(max_length=50)
	base_word = models.CharField(max_length=50)
	input_word = models.CharField(max_length=50)
	times_confirmed = models.IntegerField(default=0)
	times_rejected = models.IntegerField(default=0)

class ConcretenessStat(models.Model):
	word = models.CharField(max_length=50)
	index = models.IntegerField(default=0)
	sem_rel = models.CharField(max_length=50)
	avg_score = models.FloatField(default=0.0)
	total_score = models.FloatField(default=0.0)
	rounds_played = models.IntegerField(default=0)
	
class Relation(models.Model):
	type = models.CharField(max_length=50)
	base_word = models.CharField(max_length=50)
	input_word = models.CharField(max_length=50)
	in_word_net = models.BooleanField(default=False)
	challenge_accepted = models.BooleanField(default=False)


	def __str__(self):
		return ', '.join([self.type, self.base_word, self.input_word])

class UserInput(models.Model):
	user = models.ForeignKey(User)
	round_number = models.IntegerField()
	relation = models.ForeignKey(Relation)
	word_score = models.FloatField()

class Challenge(models.Model):
	user = models.ForeignKey(User)
	relation = models.ForeignKey(Relation)
	sentence = models.CharField(max_length=140)
	is_pending = models.BooleanField()

class Pass(models.Model):
	TYPES = (
		('hyponyms', 'hyponyms'),
		('meronyms', 'meronyms'),
		('antonyms', 'antonyms'),
		('synonyms', 'synonyms'),
		('concreteness', 'concreteness'),
		('pictures', 'pictures')
	)
	user = models.ForeignKey(User)
	base_word = models.CharField(max_length=50)
	type = models.CharField(max_length=50, choices=TYPES)