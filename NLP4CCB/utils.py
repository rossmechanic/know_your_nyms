import json
import os
from NLP4CCB_Django_App import settings
from models import UserInput, UserStat, Relation
from django.core.exceptions import ObjectDoesNotExist
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

# Bonus for word appearing in WordNet
word_net_bonus = 50.0
challenge_bonus = 75.0


def score_words(base_word, input_words, sem_rel, relations_percentages):
	input_words = clean_input_words(input_words)
	words_to_wn_bonuses = word_net(base_word, input_words, sem_rel)
	words_to_ch_bonuses = confirmed_relations(base_word, input_words, sem_rel)
	relations_percentages = dict(relations_percentages) # Need to DICT THAT
	words_to_esp_scores = get_esp_scores(input_words, relations_percentages)
	return {word: {'esp_score': words_to_esp_scores[word],
				   'word_net_bonus': words_to_wn_bonuses[word],
				   'challenge_bonus': words_to_ch_bonuses[word],
				   'total_score': words_to_esp_scores[word] + words_to_wn_bonuses[word] + words_to_ch_bonuses[word]
				   } for word in input_words}


def clean_input_words(input_words):
	input_words = [str(word).lower() for word in input_words]
	input_words_stemmed = set()
	cleaned_input_words = []
	# Remove duplicates, according to the stemming
	for word in input_words:
		if word and stemmer.stem(word) not in input_words_stemmed:
			cleaned_input_words.append(word)
			input_words_stemmed.add(stemmer.stem(word))
	return cleaned_input_words


def word_net(base_word, input_words, sem_rel):
	json_f = 'data/wordnet_' + sem_rel + '.json'
	# Now will get json data of known meronym pairs.
	known_pairs = json.load(open(os.path.join(settings.STATIC_ROOT, json_f)))
	# Accesses word pairs in WordNet. If none exist, gives an empty list.
	base_word_pairs = known_pairs.get(base_word,[])
	base_word_pairs = [stemmer.stem(str(word).lower()) for word in base_word_pairs]
	# Don't return the stemmed word
	words_to_word_net = {word: True if stemmer.stem(word) in base_word_pairs else False for word in input_words}
	words_to_wn_bonuses = {k: word_net_bonus if v else 0.0 for k, v in words_to_word_net.items()}
	return words_to_wn_bonuses


def confirmed_relations(base_word, input_words, sem_rel):
	challenge_bonuses = {}
	for word in input_words:
		try:
			relation = Relation.objects.get(type=sem_rel, base_word=base_word, input_word=word)
			if relation.challenge_accepted:
				challenge_bonuses[word] = challenge_bonus
			else:
				challenge_bonuses[word] = 0.0
		except ObjectDoesNotExist:
			challenge_bonuses[word] = 0.0
	return challenge_bonuses


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
	times_played = user_inputs.values('user', 'round_number').distinct().count()
	# Percentage of players that said a relation
	percentages = [(word, round((float(input_word_dict[word]) / times_played), 3)) for word in input_word_dict]
	percentages.sort(key=lambda x: x[1])
	return percentages[::-1]


def get_esp_scores(input_words, relations_percentages):
	# Maps word stems to their words in the relations_percentages
	stem_dict = {stemmer.stem(word): word for word in relations_percentages.keys()}
	# For each input_word, if its stem appears in the stems of the words seen, map the word
	# to the percentage of the word already seen with that stem
	return {word:relations_percentages[stem_dict[stemmer.stem(word)]]*100 if stemmer.stem(word) in stem_dict else 0
									for word in input_words }


def store_round(sem_rel, base_word, word_scores, user):
	round_score = 0
	try:
		user_stat = UserStat.objects.get(user=user)
	except ObjectDoesNotExist:
		user_stat = UserStat.objects.create(user=user)
		user_stat.save()
	user_stat.rounds_played += 1
	user_stat.index += 1

	for word in word_scores:
		word_score = word_scores[word]['total_score']
		round_score += word_score
		try:
			relation = Relation.objects.get(type=sem_rel, base_word=base_word, input_word=word)
		except ObjectDoesNotExist:
			relation = Relation.objects.create(type=sem_rel, base_word=base_word, input_word=word)
			relation.save()
		user_input = UserInput.objects.create(user=user,
											  round_number=user_stat.rounds_played,
											  relation=relation,
											  word_score=word_score)

		user_input.save()

	user_stat.total_score += round_score
	user_stat.save()

def starts_with_vowel(word):
	vowels = ['A','E','I','O','U','a','e','i','o','u']
	return word[0] in vowels
