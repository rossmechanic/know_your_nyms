import json
import os
import sets
import random
from NLP4CCB_Django_App import settings
from models import UserInput, UserStat, Relation, Pass, CompletedStat, WordStat, ConfirmationStat
from django.core.exceptions import ObjectDoesNotExist
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

# Bonus for word appearing in WordNet
word_net_bonus = 50.0
challenge_bonus = 0.0


def score_words(base_word, input_words, sem_rel, relations_percentages):
	input_words = clean_input_words(input_words)
	words_to_wn_bonuses = word_net(base_word, input_words, sem_rel)
	words_to_ch_bonuses = confirmed_relations(base_word, input_words, sem_rel)
	relations_percentages = dict(relations_percentages) # Need to DICT THAT
	words_to_esp_scores = get_esp_scores(input_words, relations_percentages)
	words_to_total_scores = {word: words_to_esp_scores[word] + words_to_wn_bonuses[word] + words_to_ch_bonuses[word]
							 for word in input_words}

	input_words_scores = words_to_total_scores.items()
	input_words_scores.sort(key=lambda x: x[1], reverse=True)
	input_words = [a for (a,b) in input_words_scores]
	return [(word, {'esp_score': words_to_esp_scores[word],
				   'word_net_bonus': words_to_wn_bonuses[word],
				   'challenge_bonus': words_to_ch_bonuses[word],
				   'total_score': words_to_total_scores[word]
					} ) for word in input_words]

def score_conf_words (sem_rel, base_word, word_set, results):
	word_scores = list()
	i = 0
	if len(results) > 0:
		while i < 25 and results[i] != 0:
			stat = get_or_create_conf_stat(sem_rel, base_word, word_set[i])
			if exists_relation(sem_rel, base_word, word_set[i]):
				correct = int_to_bool(results[i])
			else:
				correct = stat.times_rejected == stat.times_confirmed or int_to_bool(results[i]) == (stat.times_confirmed > stat.times_rejected)
			word_scores.append((word_set[i], int_to_yn(results[i]), 10 if correct else 0))
			i += 1
	return word_scores

def clean_input_words(input_words):
	input_words = [str(word).lower() for word in input_words]
	input_words_stemmed = set()
	cleaned_input_words = []
	# Remove duplicates, according to the stemming
	for word in input_words:
		if word and stemmer.stem(word) not in input_words_stemmed:
			cleaned_input_words.append(word)
			input_words_stemmed.add(stemmer.stem(word))
	return cleaned_input_words


def word_net(base_word, input_words, sem_rel):
	json_f = 'data/wordnet_' + sem_rel + '.json'
	# Now will get json data of known meronym pairs.
	known_pairs = json.load(open(os.path.join(settings.STATIC_ROOT, json_f)))
	# Accesses word pairs in WordNet. If none exist, gives an empty list.
	base_word_pairs = known_pairs.get(base_word,[])
	base_word_pairs = [stemmer.stem(str(word).lower()) for word in base_word_pairs]
	# Don't return the stemmed word
	words_to_word_net = {word: True if stemmer.stem(word) in base_word_pairs else False for word in input_words}
	words_to_wn_bonuses = {k: word_net_bonus if v else 0.0 for k, v in words_to_word_net.items()}
	return words_to_wn_bonuses


def confirmed_relations(base_word, input_words, sem_rel):
	challenge_bonuses = {}
	for word in input_words:
		try:
			relation = Relation.objects.get(type=sem_rel, base_word=base_word, input_word=word)
			if relation.challenge_accepted:
				challenge_bonuses[word] = challenge_bonus
			else:
				challenge_bonuses[word] = 0.0
		except ObjectDoesNotExist:
			challenge_bonuses[word] = 0.0
	return challenge_bonuses

def get_relations_percentages_no_filter(sem_rel, base_word):
	user_inputs = UserInput.objects.filter(relation__type=sem_rel, relation__base_word=base_word)
	input_words = [u.relation.input_word for u in user_inputs]
	stem_dict = {} # Maps a stem to an actual word
	input_word_dict = {}
	for w in input_words:
		# If we haven't seen this word stem, make a new entry
		if stemmer.stem(w) not in stem_dict:
			stem_dict[stemmer.stem(w)] = w
			input_word_dict[w] = 1
		# If we have, add one to the associated word for that existing stem
		else:
			input_word_dict[stem_dict[stemmer.stem(w)]] += 1

	# The number of people that have played this word
	times_played = user_inputs.values('user', 'round_number').distinct().count()
	words = [word for word in input_word_dict]

	# Percentage of players that said a relation
	percentages = [(word, round((float(input_word_dict[word]) / times_played), 3)) for word in words]
	percentages.sort(key=lambda x: x[1])
	return percentages[::-1]


def get_relations_percentages(sem_rel, base_word):
	user_inputs = UserInput.objects.filter(relation__type=sem_rel, relation__base_word=base_word)
	input_words = [u.relation.input_word for u in user_inputs]
	stem_dict = {} # Maps a stem to an actual word
	input_word_dict = {}
	for w in input_words:
		# If we haven't seen this word stem, make a new entry
		if stemmer.stem(w) not in stem_dict:
			stem_dict[stemmer.stem(w)] = w
			input_word_dict[w] = 1
		# If we have, add one to the associated word for that existing stem
		else:
			input_word_dict[stem_dict[stemmer.stem(w)]] += 1

	# The number of people that have played this word
	times_played = user_inputs.values('user', 'round_number').distinct().count()
	filtered_words = [word for word in input_word_dict]
	total = 0
	for word in filtered_words:
		if input_word_dict[word] >= 2:
			total += input_word_dict[word]
	filtered_words = filter(lambda x: float(input_word_dict[x] > 2), filtered_words)

	# Percentage of players that said a relation
	percentages = [(word, round((float(input_word_dict[word]) / total), 3)) for word in filtered_words]
	percentages.sort(key=lambda x: x[1])
	return percentages[::-1]


def get_esp_scores(input_words, relations_percentages):
	# Maps word stems to their words in the relations_percentages
	stem_dict = {stemmer.stem(word): word for word in relations_percentages.keys()}
	# For each input_word, if its stem appears in the stems of the words seen, map the word
	# to the percentage of the word already seen with that stem
	return {word: float(relations_percentages[stem_dict[stemmer.stem(word)]]*100) if stemmer.stem(word) in stem_dict else 0
									for word in input_words}

# Average score per round over all players. Each weighted equally, regardless of rounds played.
def get_overall_player_avg():
	lst = list(map(lambda x: div(x.total_score, x.rounds_played), list(UserStat.objects.all())))
	return div(sum(lst), float(len(lst)))

def get_overall_player_std_dev(avg):
	lst = list(map(lambda x: div(x.total_score, x.rounds_played), list(UserStat.objects.all())))
	sqsum = 0.0
	for a in lst:
		sqsum += (a-avg)**2.0
	return div(sqsum, float(len(lst)))

# Average score over all words. Each weighted equally, regardless of rounds played.
def get_overall_score_avg():
	lst = WordStat.objects.values_list('avg_score', flat=True)
	return div(sum(lst), float(len(lst)))

def get_overall_score_std_dev(avg):
	lst = WordStat.objects.values_list('avg_score', flat=True)
	sqsum = 0.0
	for a in lst:
		sqsum += (a-avg)**2.0
	return div(sqsum, float(len(lst)))

# Adds a relation object to the database
def create_relation(sem_rel, base_word, word):
	try:
		relation = Relation.objects.get(type=sem_rel, base_word=base_word, input_word=word)
	except ObjectDoesNotExist:
		relation = Relation.objects.create(type=sem_rel, base_word=base_word, input_word=word)
		relation.save()
	return relation

def exists_relation(sem_rel, base_word, word):
	try:
		relation = Relation.objects.get(type=sem_rel, base_word=base_word, input_word=word)
		return True;
	except ObjectDoesNotExist:
		return False

def get_or_create_conf_stat(sem_rel, base_word, word):
	try:
		relation = ConfirmationStat.objects.get(sem_rel=sem_rel, base_word=base_word, input_word=word)
	except ObjectDoesNotExist:
		relation = ConfirmationStat.objects.create(sem_rel=sem_rel, base_word=base_word, input_word=word)
		relation.save()
	return relation

# Creates or edits a confirmation relation.
def confirm_or_reject_relation(sem_rel, base_word, word, decision):
	try:
		relation = ConfirmationStat.objects.get(sem_rel=sem_rel, base_word=base_word, input_word=word)
		if decision == 1:
			relation.times_confirmed += 1
		elif decision == 0: 
			relation.times_rejected += 1
	except ObjectDoesNotExist:
		relation = ConfirmationStat.objects.create(sem_rel=sem_rel, base_word=base_word, input_word=word)
	relation.save()

# Save results of a round of the confirmation game
def save_conf_scores(word_set, decisions, sem_rel, base_word):
	for i in range(len(decisions)):
		confirm_or_reject_relation(sem_rel, base_word, word_set[i], decisions[i])

# Storing data on a round from an authenticated player
# Updates user_stat
def store_round(sem_rel, base_word, index, word_scores, request):
	user = request.user
	round_score = 0
	user_stat = get_or_create_user_stat(user)
	try:
		user_stat = UserStat.objects.get(user=user)
	except ObjectDoesNotExist:
		user_stat = UserStat.objects.create(user=user)
		user_stat.save()
	user_stat.rounds_played += 1
	
	nonempty = False

	# Creates a relation to save in the database, and a UserInput object
	for word,scores in word_scores:
		nonempty = True
		word_score = scores['total_score']
		round_score += word_score
		relation = create_relation(sem_rel, base_word, word)
		user_input = UserInput.objects.create(user=user,
											  round_number=user_stat.rounds_played,
											  relation=relation,
											  word_score=word_score)

		user_input.save()
	# Update the statistics for this word with new data. Adds a score bonus if this word has not been played 5 times yet
	word_stat = get_or_create_word_stat(base_word, sem_rel, index)
	if word_stat.rounds_played <= 5 and nonempty:
		round_score += 40
	save_word_result(base_word, sem_rel, round_score)
	user_stat.total_score += round_score
	user_stat.save()

# Storing data on a round from an unauthenticated player
def anon_store_round(sem_rel, base_word, index, word_scores):
	round_score = 0

	# Creates a relation to save in the database
	# Player is anonymous, so we have no user data to save.
	for word,scores in word_scores:
		word_score = scores['total_score']
		round_score += word_score
		create_relation(sem_rel, base_word, word)

	# Update the statistics for this word with new data. Adds a score bonus if this word has not been played 5 times yet
	word_stat = get_or_create_word_stat(base_word, sem_rel, index)
	if word_stat.rounds_played <= 5:
		round_score += 40
	save_word_result(base_word, sem_rel, round_score)


def starts_with_vowel(word):
	vowels = ['A', 'E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u']
	return word[0] in vowels

def get_or_create_user_stat(user):
	try:
		user_stat = UserStat.objects.get(user=user)
	except ObjectDoesNotExist:
		user_stat = UserStat.objects.create(user=user)
		user_stat.save()
	return user_stat

def get_or_create_word_stat(word, rel, i):
	try:
		word_stat = WordStat.objects.get(word=word, sem_rel=rel, index=i)
	except ObjectDoesNotExist:
		word_stat = WordStat.objects.create(word=word, sem_rel=rel, index=i)
		word_stat.save()
	return word_stat

# Updates the stats of a word with a new score
def save_word_result(word, sem_rel, score):
	try:
		word_stat = WordStat.objects.get(word=word, sem_rel=sem_rel)
		word_stat.avg_score = (word_stat.avg_score * word_stat.rounds_played + score)/(word_stat.rounds_played + 1)
		word_stat.rounds_played = word_stat.rounds_played + 1
		word_stat.save()
	except ObjectDoesNotExist:
		return
# Adds a CompletedStat object for this word to the database. Used to determine if a player has completed a word or not
def mark_played(user, index, word, sem_rel):
	try:
		cset = CompletedStat.objects.filter(user=user, sem_rel=sem_rel, index=index, base_word=word)
		cmp_stat = CompletedStat.objects.get(user=user, sem_rel=sem_rel, index=index, base_word=word)
	except ObjectDoesNotExist:
		cmp_stat = CompletedStat.objects.create(user=user, sem_rel=sem_rel, index=index, base_word=word)
		cmp_stat.save()


def skip_word(request):
	sem_rel = request.POST['sem_rel']
	base_word = request.POST['base_word']
	index = request.POST['word_index']

	pass_object = Pass.objects.create(user=request.user, type=sem_rel, base_word=base_word)
	pass_object.save()

	passes = Pass.objects.filter(type=sem_rel, base_word=base_word).distinct().count()
	plays = get_or_create_word_stat(base_word, sem_rel, index).rounds_played

	# If the ratio between passes and plays gets too large, we retire words, meaning they won't be selected dynamically again.
	if passes + plays >= 30 and passes > 3*plays:
		word_stat = get_or_create_word_stat(base_word, sem_rel, index)
		word_stat.retired = True
		word_stat.save()
	elif passes + plays >= 30:
		word_stat = get_or_create_word_stat(base_word, sem_rel, index)
		word_stat.retired = False
		word_stat.save()

# Rank given a sorted list.
def rank(user_stat_arr, user_stat, getStat, lo, hi):
	if len(user_stat_arr) == 0:
		return -1
	mid = (lo + hi)//2
	if lo == hi and user_stat_arr[lo].user.username == user_stat.user.username:
		return lo
	elif lo == hi:
		return -1
	if getStat(user_stat) == getStat(user_stat_arr[mid]):
		if user_stat_arr[lo].user.username == user_stat.user.username:
			return mid
		return rank(user_stat_arr, user_stat, getStat, mid + 1, hi) + rank(user_stat_arr, user_stat, getStat, lo, mid) + 1
	elif getStat(user_stat) > getStat(user_stat_arr[mid]):
		return rank(user_stat_arr, user_stat, getStat, lo, mid)
	elif getStat(user_stat) < getStat(user_stat_arr[mid]):
		return rank(user_stat_arr, user_stat, getStat, mid + 1, hi)


# Divides two numbers, but returns 0 if it would divide by zero.
def div(a, b):
	return 0 if b == 0 else a/b

def random_select_unplayed_word(vocab_size, sem_rel):
	unplayed = sets.Set()
	for i in range (0, vocab_size):
		unplayed.add(i)
	# The unplayed words are ones with no statistics created yet.
	for word_stat in WordStat.objects.filter(sem_rel=sem_rel):
		if word_stat.index in unplayed:
			unplayed.remove(word_stat.index)
	return random.choice(tuple(unplayed))


def dynamic_select_word(user, vocab_size, sem_rel, ind):
	# We create a set of indices of words that this player could play, and narrow it down as we go
	# Initially all words in this relationship are prospective choices
	word_choices = sets.Set()
	for stat in WordStat.objects.filter(sem_rel=sem_rel):
		word_choices.add(stat.index)


	# If the user is authenticated, gather data on their average score relative to the rest of the playerbase	
	if user.is_authenticated():
		user_stat = get_or_create_user_stat(user)
		player_avg = div(user_stat.total_score, user_stat.rounds_played)
		overall_player_avg = get_overall_player_avg()
		overall_player_std_dev = get_overall_player_std_dev(overall_player_avg)
		z_score = div((player_avg - overall_player_avg), overall_player_std_dev)

		# Use that information about the player's relative rank to select a question with similarly 
		# difficulty relative to other questions
		question_avg = get_overall_score_avg()
		question_std_dev = get_overall_score_std_dev(question_avg)
		goal_question_avg = question_avg - z_score * question_std_dev

		# Remove completed questions from prospective choices
		done = CompletedStat.objects.filter(user=user, sem_rel=sem_rel).filter().values_list('index', flat=True)

		for i in done:
			if i in word_choices:
				word_choices.remove(i)

		# Remove questions too far from the goal score, calculated above
		# Also remove questions that are retired.
		unviable = list(filter(lambda x: abs(x.avg_score - goal_question_avg) > .3 * question_std_dev or x.retired, 
		list(WordStat.objects.filter(sem_rel=sem_rel))))
		unviable_ind = list(map(lambda x: x.index, unviable))
		for i in unviable_ind:
			if i in word_choices:
				word_choices.remove(i)
		
		# Remove passed questions from prospective choices
		passed = Pass.objects.filter(user=user, type=sem_rel)

		for p in passed:
			if ind[p.base_word, sem_rel] in word_choices:
				word_choices.remove(ind[p.base_word, sem_rel])		
			
	# If there are no words close enough to the desired average score, we just pick a random one. 
	if len(word_choices) == 0:
		return random.randint(0, vocab_size - 1)

	# Otherwise pick a random one from the viable set of questions.	
	# If the user isn't authenticated, any word is valid as none are removed from 'word_choices'. So it effectively picks a random word.
	return random.choice(tuple(word_choices))

def find_base_word(base_words, sem_rel):
	available = list()
	bw_rel_count = dict()
	for rel in Relation.objects.filter(type=sem_rel):
		if rel.base_word not in bw_rel_count:
	 		bw_rel_count[rel.base_word] = 1
	 	else:
	 		bw_rel_count[rel.base_word] += 1
	for base_word in bw_rel_count:
	 	if bw_rel_count[base_word] >= 5:
	 		available.append(base_word)
	if len(available) == 0:
		return random.choice(base_words)

	return random.choice(available)

def find_word_pairs(base_word, sem_rel, top_words):
	play_words = list()
	# The model only predicted values/words for single words, not multi-word phrases

	# The model didn't make a prediction on this base word.
	if " " in base_word:
		print("hi")
	# The model made predictions, so we use those to find words to play.
	else:
		# Words are chosen with probability proportional to their score.
		word_scores = dict()
		for (a,b) in top_words[(sem_rel, base_word)]:
			word_scores[a] = b
		total = 0
		for word in word_scores:
			total += word_scores[word]

		existing_rels = Relation.objects.filter(type=sem_rel, base_word=base_word)
		to_use = random.randint(min(2, len(existing_rels)), min(15, len(existing_rels)))
		used_rels = random.sample(existing_rels, to_use)
		for rel in used_rels:
			play_words.append(rel.input_word)

		while len(play_words) < 25:
			rand = random.uniform(0, total)
			for word in word_scores:
				rand -= word_scores[word]
				if rand < 0:
					total -= word_scores[word]
					play_words.append(word)
					del word_scores[word]
					break

	random.shuffle(play_words)
	return play_words

def int_to_bool(i):
	if i == 1:
		return True
	else:
		return False
def int_to_yn(i):
	if i == 1:
		return "Yes"
	else:
		return "No"

def add_det(phrase, base_word, sem_rel, determiners):
	if sem_rel == 'hyponyms' or sem_rel == 'meronyms':
		if base_word in determiners:
			return phrase + determiners[base_word]
		elif starts_with_vowel(base_word):
			return phrase + 'an '
		else:
			return phrase + 'a '
	return phrase









