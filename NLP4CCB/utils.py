import json
import os
from NLP4CCB_Django_App import settings
from models import UserInput, UserStat, Relation
from django.core.exceptions import ObjectDoesNotExist
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()


def get_matched_pairs_scores(base_word, input_words, sem_rel):
	json_f = 'data/wordnet_' + sem_rel + '.json'
	# Now will get json data of known meronym pairs.
	known_pairs = json.load(open(os.path.join(settings.STATIC_ROOT, json_f)))
	# Accesses word pairs in WordNet. If none exist, gives an empty list.
	base_word_pairs = known_pairs.get(base_word,[])
	base_word_pairs = [stemmer.stem(str(word).lower()) for word in base_word_pairs]
	input_words = [str(word).lower() for word in input_words]
	input_words_stemmed = set()
	final_input_words = [] # The actual input word list to traverse
	# Remove duplicates, according to the stemming
	for word in input_words:
		if stemmer.stem(word) not in input_words_stemmed:
			final_input_words.append(word)
			input_words_stemmed.add(stemmer.stem(word))

	# Don't return the stemmed word
	pairs_and_scores = {word: 1 if stemmer.stem(word) in base_word_pairs else 0 for word in final_input_words if word}
	return pairs_and_scores


def store_round(sem_rel, base_word, words_and_scores, user):
	round_score = 0
	try:
		user_stat = UserStat.objects.get(user=user)
	except ObjectDoesNotExist:
		user_stat = UserStat.objects.create(user=user)
		user_stat.save()
	user_stat.rounds_played += 1

	for word, score in words_and_scores.items():
		round_score += score
		try:
			relation = Relation.objects.get(type=sem_rel, base_word=base_word, input_word=word)
		except ObjectDoesNotExist:
			relation = Relation.objects.create(type=sem_rel, base_word=base_word, input_word=word, word_net_score=score)
			relation.save()
		user_input = UserInput.objects.create(user=user,
											  round_number=user_stat.rounds_played,
											  relation=relation,
											  word_score=score)

		user_input.save()

	user_stat.total_score += round_score
	user_stat.save()

def get_relations_percentages(sem_rel, base_word):
	user_inputs = UserInput.objects.filter(relation__type=sem_rel, relation__base_word=base_word)
	input_words = [u.relation.input_word for u in user_inputs]
	stem_dict = {} # Maps a stem to an actual word
	input_word_dict = {}
	for w in input_words:
		# If we haven't seen this word stem, make a new entry
		if stemmer.stem(w) not in stem_dict:
			stem_dict[stemmer.stem(w)] = w
			input_word_dict[w] = 1
		# If we have, add one to the associated word for that existing stem
		else:
			input_word_dict[stem_dict[stemmer.stem(w)]] += 1

	# The number of people that have played this word
	times_played = user_inputs.values('user').distinct().count()
	# Percentage of players that said a relation
	percentages = [(word, float(input_word_dict[word]) / times_played) for word in input_word_dict]
	percentages.sort(key=lambda x: x[1])
	return percentages[::-1]
