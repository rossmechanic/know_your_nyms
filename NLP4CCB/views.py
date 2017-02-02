from django.shortcuts import *
from models import WordRelationshipForm
from django.forms import formset_factory
import utils
import random


# Create your views here.
def index(request):
	word_relationship_formset = formset_factory(WordRelationshipForm, extra=1)
	word_list = ['computer','fish','face','hand','person','dog']
	selected_word = random.choice(word_list)
	context = {
		"title": "NLP4CCB",
		"formset": word_relationship_formset,
		"base_word": selected_word
	}
	return render(request, 'input_words.html', context)

def scoring(request):
	# if this is a POST request, we need to process the form data
	if request.method == 'POST':
		base_word = request.POST['base_word']
		num_forms_returned = int(request.POST['form-TOTAL_FORMS'])
		input_words = [request.POST["form-%s-word" % i] for i in range(num_forms_returned)]
		context = {}
		# Creates scores based on the words and the semantic relationship
		context['base_word'] = base_word
		context['words_and_scores'] = utils.get_matched_pairs_scores(base_word, input_words, 'meronyms')

		print context
		return render(request, 'scoring.html', context)
	else:
		return redirect('/models/')