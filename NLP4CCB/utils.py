import json
import os
from NLP4CCB_Django_App import settings


def get_matched_pairs_scores(base_word, input_words, sem_rel):
	json_f = 'data/wordnet_' + sem_rel + '.json'
	# Now will get json data of known meronym pairs.
	known_meronym_pairs = json.load(open(os.path.join(settings.STATIC_ROOT, json_f)))
	# Pairs for "person". Hardcoded for now. Should access the appropriate base word in the future.
	base_word_meronyms = known_meronym_pairs[base_word]
	pairs_and_scores = {word: 1 if word in base_word_meronyms else 0 for word in input_words if word}
	return pairs_and_scores
