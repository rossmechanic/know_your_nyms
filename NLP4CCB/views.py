from django.conf import settings
from django.shortcuts import *
from models import WordRelationshipForm
from django.forms import formset_factory
import utils
import random
import os
from django.contrib.auth.decorators import login_required
from models import UserStat
from django.core.exceptions import ObjectDoesNotExist

# Read in the vocabulary to traverse
relationships = ['synonyms','antonyms','hyponyms','meronyms']
vocabs = {}
for rel in relationships:
	vocab_file = 'data/' + rel + '_vocab.txt'
	with open(os.path.join(settings.STATIC_ROOT, vocab_file)) as f:
		lines = f.readlines()
	vocabs[rel] = [word.lower().strip() for word in lines]

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

def index(request):
	try:
		user_stat = UserStat.objects.get(user=request.user)
	except ObjectDoesNotExist:
		user_stat = UserStat.objects.create(user=request.user)
		user_stat.save()
	context = dict()
	context['rounds_played'] = user_stat.rounds_played
	context['average_score'] = round(user_stat.total_score / user_stat.rounds_played, 2)
	return render(request, 'welcome.html', context)


@login_required
def models(request):
	word_relationship_formset = formset_factory(WordRelationshipForm, extra=1)
	# sem_rel = random.choice(['meronyms','hyponyms'])
	sem_rel = 'meronyms'
	# The question and list of base words are specific to the selected relationship type
	question = rel_q_map[sem_rel]
	vocab = vocabs[sem_rel]
	user_stat = utils.get_or_create_user_stat(request)
	vocab_index = user_stat.index
		# utils.rel_index(sem_rel, user_stat)
	# Go in a set order for the vocabulary for each user.
	if vocab_index < len(vocab):
		base_word = vocab[vocab_index]
	else:
		base_word = random.choice(vocab)
	# Handle word starting with a vowel
	starts_vowel = utils.starts_with_vowel(base_word)
	if starts_vowel:
		question += 'an '
	else:
		question += 'a '
	context = {
		"title": "Know Your Nyms?",
		"formset": word_relationship_formset,
		"base_word": base_word,
		"sem_rel": sem_rel,
		"question": question,
		"starts_vowel": starts_vowel
	}
	return render(request, 'input_words.html', context)


@login_required
def scoring(request):
	# if this is a POST request, we need to process the form data
	if request.method == 'POST':
		sem_rel = request.POST['sem_rel']
		base_word = request.POST['base_word']
		num_forms_returned = int(request.POST['form-TOTAL_FORMS'])
		input_words = [request.POST["form-%s-word" % i] for i in range(num_forms_returned)]
		context = {}
		# Creates scores based on the words and the semantic relationship
		context['base_word'] = base_word

		relations_percentages = utils.get_relations_percentages(sem_rel, base_word)
		context['percentages'] = relations_percentages
		word_scores = utils.score_words(base_word, input_words, sem_rel, relations_percentages)
		context['word_scores'] = word_scores
		round_total = sum([word_scores[word]['total_score'] for word in word_scores])
		context['round_total'] = round_total
		answer = rel_a_map[sem_rel]
		if sem_rel == 'hyponyms' or sem_rel == 'meronyms':
			starts_vowel = utils.starts_with_vowel(base_word)
			if starts_vowel:
				answer += 'an '
			else:
				answer += 'a '
		answer += base_word
		context['answer'] = answer
		utils.store_round(sem_rel, base_word, word_scores, request.user)
		return render(request, 'scoring.html', context)
	else:
		return redirect('/models/')
