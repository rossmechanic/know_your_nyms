from django.core.management.base import BaseCommand
from NLP4CCB_Django_App import settings
import os
import json
from django.contrib.auth.models import User


class Command(BaseCommand):
	help = 'Adds n mturk accounts to the database and creates a csv of those usernames and passwords'

	def add_arguments(self, parser):
		parser.add_argument('num_turkers', nargs='+', type=int)

	# def handle(self, *args, **options):
		# f
