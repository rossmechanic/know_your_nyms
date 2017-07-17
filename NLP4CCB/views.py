import json
import os
import random
import re
import sets
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import *
from django.core.exceptions import ObjectDoesNotExist

import utils
import sets
from datetime import date
from datetime import timedelta
from models import UserInput
from models import WordRelationshipForm
from models import UserStat
from models import CompletedStat
from models import WordStat

# Read in the vocabulary to traverse
relationships = ['synonyms','antonyms','hyponyms','meronyms']
vocabs = {}
for rel in relationships:
	vocab_file = 'data/' + rel + '_base_words.txt'
	with open(os.path.join(settings.STATIC_ROOT, vocab_file)) as f:
		lines = f.readlines()
	vocabs[rel] = [word.lower().strip() for word in lines]

# Set up a map from words to their determiners, a/an/the/etc
determiners = dict()
pat = re.compile(r'(?P<word>[0-9a-zA-Z ]+)=(?P<det>\S*)$')
det_rels = ['meronyms', 'hyponyms']
for rel in det_rels:
	det_file = 'data/' + rel + '_determiners.txt'
	for line in open(os.path.join(settings.STATIC_ROOT, det_file)):
		res = pat.match(line)
		if res:
			p = res.group('det')
			word = res.group('word')
			if p == '':
				determiners[word] = p
			else:
				determiners[word] = p + ' '

# Map from words to their index.
ind = dict()
for rel in relationships:
	for i in range (0, len(vocabs[rel])):
		ind[vocabs[rel][i], rel] = i

# Map from base words to the top 100 model predictions and their scores
top_words = dict()
pat = re.compile(r'(?P<base_word>[0-9a-zA-Z ]+)\t(?P<sem_rel>(meronyms|hyponyms|synonyms|antonyms))\t(?P<word>[0-9a-zA-Z ]+)\t(?P<score>0.[0-9]+)$')
for rel in relationships:
	pred_file = 'data/predictions_' + rel + '_top100.txt'
	for line in open(os.path.join(settings.STATIC_ROOT, pred_file)):
		res = pat.match(line)
		if res:
			sem_rel = res.group('sem_rel')
			base_word = res.group('base_word')
			if (sem_rel,base_word) not in top_words:
				top_words[(sem_rel,base_word)] = list()
			top_words[(sem_rel,base_word)].append((res.group('word'), float(res.group('score'))))

conc_rating = dict()
conc_file = 'data/concreteness_ratings.txt'
ignorefirst = True
for line in open(os.path.join(settings.STATIC_ROOT, conc_file)):
	if not ignorefirst:
		words = line.split('\t')
		base_word = words[0]
		conc_mean = float(words[2])
		percent_known = float(words[6])
		in_base_words = False
		for rel in relationships:
			if (base_word,rel) in ind and not in_base_words:
				conc_rating[base_word] = (conc_mean, percent_known)
				in_base_words = True
	else:
		ignorefirst = False

# Dictionary for sem_rel to question
rel_q_map = {'synonyms': 'What is another word for ',
			 'antonyms': 'What is the opposite of ',
			 'hyponyms': 'What are kinds of ',
			 'meronyms': 'What are parts of '
			 }

rel_a_map = {'synonyms': 'Another word for ',
			 'antonyms': 'The opposite of ',
			 'hyponyms': 'Kinds of ',
			 'meronyms': 'Parts of '
			 }

# For the nym or not game
rel_p_map = {'synonyms': 'Does this mean the same as ',
			 'antonyms': 'Is this the opposite of ',
			 'hyponyms': 'Is this a kind of ',
			 'meronyms': 'Is this a part of '
			 }

# Dictionary for sem_rel to amount of time on timer:
rel_time_map = {
	'synonyms': 10,
	'antonyms': 10,
	'hyponyms': 15,
	'meronyms': 20
}

def index(request):
	context = dict()
	if request.user.is_authenticated():
		user_stat = utils.get_or_create_user_stat(request.user)
		context['rounds_played'] = user_stat.rounds_played
		context['total_score'] = round(user_stat.total_score, 2)
		if context['rounds_played'] <= 0:
			context['average_score'] = 0
		else:
			context['average_score'] = round(user_stat.total_score / user_stat.rounds_played, 2)
	return render(request, 'welcome.html', context)

def models(request):
	word_relationship_formset = formset_factory(WordRelationshipForm, extra=1)
	if request.user.is_authenticated:
		user_stat = utils.get_or_create_user_stat(request.user)
		user_stat.last_login = date.today()
		user_stat.save()

	# We should select a relationship randomly from the set of selected ones. If none were selected,
	# just choose randomly for all (unless we want some javascript solution)
	if request.method == 'POST':
		if 'skip' in request.POST:
			if request.user.is_authenticated():
				utils.skip_word(request, conc_rating)
			return HttpResponse("Success")
		else:
			new_rels = request.POST.getlist('checks')
			request.session['relationships'] = new_rels
	rel_options = request.session['relationships'] if request.session['relationships'] else ['meronyms', 'antonyms', 'hyponyms', 'synonyms']
	sem_rel = random.choice(list(map(lambda x: str(x), rel_options)))

	# The question and list of base words are specific to the selected relationship type
	question = rel_q_map[sem_rel]
	vocab = vocabs[sem_rel]
	# 20% of the time pick a random unplayed word, otherwise dynamically select one based on user stats.
	if random.random() <= 0.2:
		vocab_index = utils.random_select_unplayed_word(len(vocab), sem_rel)
	else:
		vocab_index = utils.dynamic_select_word(request.user, len(vocab), sem_rel, ind)
	base_word = vocab[vocab_index]

	# Add the correct determiner to a word
	question = utils.add_det(question, base_word, sem_rel, determiners)

	context = {
		"title": "Know Your Nyms?",
		"formset": word_relationship_formset,
		"base_word": base_word,
		"word_index": vocab_index,
		"sem_rel": sem_rel,
		"question": question,
		"time": rel_time_map[sem_rel]
	}
	return render(request, 'input_words.html', context)

def scoring(request):
	# if this is a POST request, we need to process the form data
	if request.method == 'POST':
		sem_rel = request.POST['sem_rel']
		base_word = request.POST['base_word']
		index = request.POST['word_index']

		# If the user is authenticated, mark this word as played.
		if request.user.is_authenticated():
			utils.mark_played(request.user, index, base_word, sem_rel)

		num_forms_returned = int(request.POST['form-TOTAL_FORMS'])
		input_words = [request.POST["form-%s-word" % i] for i in range(num_forms_returned)]
		context = {}
		# Creates scores based on the words and the semantic relationship
		context['base_word'] = base_word

		relations_percentages = utils.get_relations_percentages(sem_rel, base_word)
		context['percentages'] = {'data': [{'word': str(word), 'percentage': pct} for word, pct in relations_percentages[:5]]}
		# Now a list of tuples (word,dict), not a dictionary itself
		word_scores = utils.score_words(base_word, input_words, sem_rel, relations_percentages)
		context['word_scores'] = word_scores
		round_total = sum([scores['total_score'] for word,scores in word_scores])

		# If this word has been played less than 5 times, give the user a bonus
		# 1 form returned means that no words were submitted
		word_stat = utils.get_or_create_word_stat(base_word, sem_rel, index)
		first_response_bonus = 40 if word_stat.rounds_played <= 5 and (num_forms_returned > 1 or input_words[0] != '') else 0
		if request.user.is_authenticated():
			user_stat = utils.get_or_create_user_stat(request.user)
		context['first_response_bonus'] = first_response_bonus
		context['round_total'] = round_total + first_response_bonus

		user_inputs = UserInput.objects.filter(relation__type=sem_rel, relation__base_word=base_word)
		context['times_played'] = user_inputs.values('user', 'round_number').distinct().count()
		answer = rel_a_map[sem_rel]

		answer = utils.add_det(answer, base_word, sem_rel, determiners)
		answer += base_word
		context['answer'] = answer

		# If the user is authenticated, store their data and the new word data.
		if request.user.is_authenticated():
			utils.store_round(sem_rel, base_word, index, word_scores, request)
		# Otherwise just store the word data.
		else:
			utils.anon_store_round(sem_rel, base_word, index, word_scores)
		return render(request, 'scoring.html', context)
	else:
		return redirect('/models/')


def confirmation(request):
	word_relationship_formset = formset_factory(WordRelationshipForm)
	if request.method == 'POST':
		new_rels = request.POST.getlist('checks')
		request.session['relationships'] = new_rels

	rel_options = request.session['relationships'] if request.session['relationships'] else ['meronyms', 'antonyms', 'hyponyms', 'synonyms']
	sem_rel = random.choice(list(map(lambda x: str(x), rel_options)))

	vocab = vocabs[sem_rel]
	base_word = utils.find_base_word(vocab, sem_rel)

	phrase = rel_p_map[sem_rel]
	phrase = utils.add_det(phrase, base_word, sem_rel, determiners)

	word_set = utils.find_word_pairs(base_word, sem_rel, top_words, vocab)
	context = {
		"title": "Know Your Nyms?",
		"formset": word_relationship_formset,
		"base_word": base_word,
		"sem_rel": sem_rel,
		"word_set": {'data': [{'word': str(word)} for word in word_set]},
		"curr_word": word_set[0],
		"phrase": phrase,
		"time": 20
	}
	return render(request, 'nymornot.html', context)

def confirmation_scoring(request):
	if request.method == 'POST':
		word_set = request.POST['word_set'].split(",")

		results = list() if request.POST['results'] == '' else [int(x) for x in request.POST['results'].split(",")]

		sem_rel = request.POST['sem_rel']
		base_word = request.POST['base_word']


		context = dict()
		word_scores = utils.score_conf_words(sem_rel, base_word, word_set, results)
		round_total = 0
		for (a,b,score) in word_scores:
			round_total += score

		utils.save_conf_scores(word_set, results, sem_rel, base_word)
		context['word_scores'] = word_scores
		context['round_total'] = round_total

		answer = rel_a_map[sem_rel]
		answer = utils.add_det(answer, base_word, sem_rel, determiners)

		answer += base_word
		context['answer'] = answer

		return render(request, 'nymornot_scoring.html', context)
	else:
		return redirect('/confirmation/')

def leaderboard(request):
	context = dict()
	rnds_played_set = UserStat.objects.order_by('-rounds_played')
	total_score_set = UserStat.objects.order_by('-total_score')
	word_score_set = WordStat.objects.order_by('-avg_score')
	# Only words played 5+ times are allowed on the leaderboard
	word_score_list = list(filter(lambda x: x.rounds_played >= 10, word_score_set))

	average_score_list = list(UserStat.objects.all())
	# Only players who have played 10+ rounds are allowed on the leaderboard
	# Furthermore players who have not played in a month are not ranked for avg score.
	average_score_list = filter(lambda x: x.rounds_played >= 10, average_score_list)
	average_score_list = filter(lambda x: abs((date.today() - x.last_login).days) <= 30, average_score_list)
	average_score_list.sort(key=lambda x: utils.div(x.total_score, x.rounds_played), reverse=True)

	# If the user is authenticated, gather data on them in addition to just top players
	if request.user.is_authenticated():
		user_stat = utils.get_or_create_user_stat(request.user)
		context['rounds_played'] = user_stat.rounds_played
		context['total_score'] = round(user_stat.total_score, 2)
		context['avg_score'] = round(utils.div(user_stat.total_score, user_stat.rounds_played), 2)
		rounds_played_rank = utils.rank(rnds_played_set, user_stat, lambda x: x.rounds_played, 0, len(rnds_played_set) - 1)
		total_score_rank = utils.rank(total_score_set, user_stat, lambda x: x.total_score, 0, len(total_score_set) - 1)
		avg_score_rank = utils.rank(average_score_list, user_stat, lambda x: utils.div(x.total_score, x.rounds_played), 0, len(average_score_list) - 1)
		context['total_score_rank'] = str(total_score_rank + 1) if total_score_rank >= 0 else '-'
		context['avg_score_rank'] = str(avg_score_rank + 1) if avg_score_rank >= 0 else '-'
		context['rounds_played_rank'] = str(rounds_played_rank + 1) if rounds_played_rank >= 0 else '-'
		context['num_players'] = len(total_score_set)
	# Adding top x scores per category to context
	for i in range (0,5):
		if i < len(word_score_list):
			stat = word_score_list[i]
			context['word_rank' + str(i+1)] = stat.word
			context['word_score' + str(i+1)] = round(stat.avg_score, 2)
			context['sem_rel' + str(i+1)] = ("Synonyms of " if stat.sem_rel == 'synonyms' else 
											"Antonyms of " if stat.sem_rel == 'antonyms' else
											rel_a_map[stat.sem_rel] + determiners[stat.word])
	for i in range (0,5):
		if i < len(rnds_played_set):
			stat = rnds_played_set[i]
			context['rnd_rank' + str(i+1)] = stat.user.username
			context['rnd_score' + str(i+1)] = stat.rounds_played
	for i in range (0,5):
		if i < len(total_score_set):
			stat = total_score_set[i]
			context['ttl_rank' + str(i+1)] = stat.user.username
			context['ttl_score' + str(i+1)] = round(stat.total_score, 2)
	for i in range (0,10):
		if i < len(average_score_list):
			stat = average_score_list[i]
			context['avg_rank' + str(i+1)] = stat.user.username
			val = 0;
			if (stat.rounds_played != 0):
				val = stat.total_score/stat.rounds_played
			context['avg_score' + str(i+1)] = round(val, 2)
	return render(request, 'leaderboard.html', context)
