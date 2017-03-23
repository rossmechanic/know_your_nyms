import json
import os
from NLP4CCB_Django_App import settings
from models import User, UserInput, UserStat, Relation
from django.core.exceptions import ObjectDoesNotExist


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


def store_round(sem_rel, base_word, words_and_scores, user):
	round_score = 0
	try:
		user_stat = UserStat.objects.get(user=user)
	except ObjectDoesNotExist:
		user_stat = UserStat.objects.create(user=user, rounds_played=0, total_score=0.0)
		user_stat.save()
	user_stat.rounds_played += 1

	for word, score in words_and_scores.items():
		round_score += score
		try:
			relation = Relation.objects.get(type=sem_rel, base_word=base_word, input_word=word)
		except ObjectDoesNotExist:
			relation = Relation.objects.create(type=sem_rel, base_word=base_word, input_word=word, word_net_score=score,
											   model_score=0.0)
			relation.save()
		user_input = UserInput.objects.create(user=user,
											  round_number=user_stat.rounds_played,
											  round_time=20,
											  relation=relation,
											  word_score=score,
											  challenge=False)

		user_input.save()

	user_stat.total_score += round_score
	user_stat.save()