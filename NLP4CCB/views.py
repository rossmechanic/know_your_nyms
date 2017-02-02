from django.shortcuts import *
from models import WordRelationshipForm
from django.forms import formset_factory
import utils
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login')
def index(request):


	word_relationship_formset = formset_factory(WordRelationshipForm, extra=5)
	context = {
		"title": "NLP4CCB",
		"formset": word_relationship_formset
	}
	return render(request, 'input_words.html', context)

def sentences(request):
	# if this is a POST request, we need to process the form data
	if request.method == 'POST':
		num_forms_returned = int(request.POST['form-TOTAL_FORMS'])
		rels = []
		for i in range(num_forms_returned):
			word1 = request.POST["form-%s-word1" % i]
			word2 = request.POST["form-%s-word2" % i]
			rels.append((word1, word2))

		context = {}

		# Using absolute path for demo. Will fix this later
		context['data'] = utils.get_data_from_rels(rels)

		print context
		return render(request, 'sentences.html', context)
	else:
		return redirect('/models/')