import json
import os
from NLP4CCB_Django_App import settings


def get_matched_pairs_scores(words):
	# Now will get json data of known meronym pairs.
	known_meronym_pairs = json.load(open(os.path.join(settings.STATIC_ROOT, 'data/meronyms.json')))
	# Pairs for "person". Hardcoded for now. Should access the appropriate base word in the future.
	current_pairs = known_meronym_pairs['person']
	matched_words = [word for word in words if word in current_pairs]
	pairs_and_scores = {word: score(word) for word in matched_words}
	return pairs_and_scores

# Actual scoring to be figured out later.
def score(word):
	return 1

