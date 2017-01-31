from django.shortcuts import *
from models import WordRelationshipForm
from django.forms import formset_factory
import utils


# Create your views here.
def index(request):
	word_relationship_formset = formset_factory(WordRelationshipForm, extra=1)
	context = {
		"title": "NLP4CCB",
		"formset": word_relationship_formset
	}
	return render(request, 'input_words.html', context)

def sentences(request):
	# if this is a POST request, we need to process the form data
	if request.method == 'POST':
		print request.POST
		context = {}

		print context
		return render(request, 'sentences.html', context)
	else:
		return redirect('/models/')