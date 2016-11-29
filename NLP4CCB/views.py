from django.shortcuts import render
from models import WordRelationshipForm
from django.forms import formset_factory


# Create your views here.
def index(request):
	word_relationship_formset = formset_factory(WordRelationshipForm, extra=4)
	context = {
		"title": "NLP4CCB",
		"formset": word_relationship_formset
	}
	return render(request, 'test.html', context)

