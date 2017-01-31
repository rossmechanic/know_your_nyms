from django.shortcuts import *
from models import WordRelationshipForm
from django.forms import formset_factory
import utils


# Create your views here.
def index(request):
	words_formset = formset_factory(WordRelationshipForm, extra=1)
    word_forms = words_formset()
	context = {
		"title": "NLP4CCB",
		"formset": word_forms
	}
	return render(request, 'input_words.html', context)

def scoring(request):
	# if this is a POST request, we need to process the form data
	if request.method == 'POST':
		num_forms_returned = int(request.POST['form-TOTAL_FORMS'])
		words = []
		for i in range(num_forms_returned):
			word1 = request.POST["form-%s-word1" % i]
			words.append(word1)

		context = {}
		context['words_and_scores'] = utils.get_matched_pairs_scores(words)

		print context
		return render(request, 'scoring.html', context)
	else:
		return redirect('/models/')