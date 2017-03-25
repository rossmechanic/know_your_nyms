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

vocab_file = 'data/vocab.txt'
with open(os.path.join(settings.STATIC_ROOT, vocab_file)) as f:
    lines = f.readlines()
vocab = [word.lower().strip() for word in lines]
len_vocab = len(vocab)

def index(request):
	return render(request, 'welcome.html')


@login_required
def models(request):
	word_relationship_formset = formset_factory(WordRelationshipForm, extra=1)
	# sem_rel = random.choice(['meronyms','hyponyms'])
	sem_rel = 'meronyms'
	if sem_rel == 'meronyms':
		question = 'Name parts of a '
	elif sem_rel == 'hyponyms':
		question = 'Name kinds of a '
	# Get the user's UserStat model. Create it if it doesn't exist.
	try:
		user_stat = UserStat.objects.get(user=request.user)
	except ObjectDoesNotExist:
		user_stat = UserStat.objects.create(user=request.user, rounds_played=0, total_score=0.0)
		user_stat.save()
	rounds_played = user_stat.rounds_played
	# Go in a set order for the vocabulary for each user.
	if rounds_played < len_vocab:
		base_word = vocab[rounds_played]
	else:
		base_word = random.choice(vocab)
	context = {
		"title": "Know Your Nyms?",
		"formset": word_relationship_formset,
		"base_word": base_word,
		"sem_rel": sem_rel,
		"question": question
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
		words_and_scores = utils.get_matched_pairs_scores(base_word, input_words, sem_rel)
		score_total = sum(words_and_scores.values())
		context['words_and_scores'] = words_and_scores
		context['score_total'] = score_total

		utils.store_round(sem_rel, base_word, words_and_scores, request.user)

		return render(request, 'scoring.html', context)
	else:
		return redirect('/models/')
