import json
import os
from NLP4CCB_Django_App import settings


def get_matched_pairs_scores(base_word, input_words, sem_rel):
	json_f = 'data/wordnet_' + sem_rel + '.json'
	# Now will get json data of known meronym pairs.
	known_pairs = json.load(open(os.path.join(settings.STATIC_ROOT, json_f)))
	# Accesses word pairs in WordNet. If none exist, gives an empty list.
	base_word_pairs = known_pairs.get(base_word,[])
	print(base_word_pairs)
	pairs_and_scores = {word: 1 if str(word).lower() in map(str.lower, map(str, base_word_pairs)) else 0
															for word in input_words if word}
	return pairs_and_scores
