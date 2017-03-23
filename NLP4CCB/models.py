from __future__ import unicode_literals
from django import forms
from django.db import models


# Create your models here.

class WordRelationshipForm(forms.Form):
	word = forms.CharField(
		max_length=100,
		widget=forms.TextInput()
	)