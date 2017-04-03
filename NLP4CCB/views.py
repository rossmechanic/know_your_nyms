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
vocab_file = 'data/vocab.txt'
with open(os.path.join(settings.STATIC_ROOT, vocab_file)) as f:
    lines = f.readlines()
vocab = [word.lower().strip() for word in lines]
len_vocab = len(vocab)

def index(request):
	try:
		user_stat = UserStat.objects.get(user=request.user)
	except ObjectDoesNotExist:
		user_stat = UserStat.objects.create(user=request.user)
		user_stat.save()
	context = {}
	context['rounds_played'] = user_stat.rounds_played
	return render(request, 'welcome.html', context)


@login_required
def models(request):
	word_relationship_formset = formset_factory(WordRelationshipForm, extra=1)
	# sem_rel = random.choice(['meronyms','hyponyms'])
	sem_rel = 'meronyms'
	if sem_rel == 'meronyms':
		question = 'Name parts of '
	elif sem_rel == 'hyponyms':
		question = 'Name kinds of '
	# Get the user's UserStat model. Create it if it doesn't exist.
	try:
		user_stat = UserStat.objects.get(user=request.user)
	except ObjectDoesNotExist:
		user_stat = UserStat.objects.create(user=request.user)
		user_stat.save()
	user_index = user_stat.index
	# Go in a set order for the vocabulary for each user.
	if user_index < len_vocab:
		base_word = vocab[user_index]
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

		utils.store_round(sem_rel, base_word, word_scores, request.user)
		return render(request, 'scoring.html', context)
	else:
		return redirect('/models/')
