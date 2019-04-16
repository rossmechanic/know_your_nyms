from django.core.management.base import BaseCommand
import settings
import os
import json
from NLP4CCB.models import Relation


class Command(BaseCommand):
	help = 'Syncs current relations in the database such that the in_wordnet column is accurate'

	def handle(self, *args, **options):
		json_path = os.path.join(settings.STATIC_ROOT, 'data/wordnet_meronyms.json')
		wordnet = json.load(open(json_path, 'r'))

		for relation in Relation.objects.all():
			try:
				relation.in_word_net = relation.input_word in wordnet[relation.base_word]
				relation.save()
			except:
				continue