import json
import os
import random
from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory
from django.shortcuts import *

import settings
from . import utils
from .forms import UserForm
from .models import UserInput, UserStat, WordRelationshipForm, WordStat

with open(
    os.path.join(settings.BASE_DIR, "NLP4CCB/static/rel_to_vocab_map.json"), "r"
) as f:
    vocabs = json.load(f)

with open(
    os.path.join(settings.BASE_DIR, "NLP4CCB/static/determiner_map.json"), "r"
) as f:
    determiners = json.load(f)

with open(
    os.path.join(settings.BASE_DIR, "NLP4CCB/static/concreteness_rating.json"), "r"
) as f:
    conc_rating = json.load(f)

# Dictionary for sem_rel to question
rel_q_map = {
    "synonyms": "What is another word for ",
    "antonyms": "What is the opposite of ",
    "hyponyms": "What are kinds of ",
    "meronyms": "What are parts of ",
}

rel_a_map = {
    "synonyms": "Another word for ",
    "antonyms": "The opposite of ",
    "hyponyms": "Kinds of ",
    "meronyms": "Parts of ",
}

# For the nym or not game
rel_p_map = {
    "synonyms": "Does this mean the same as ",
    "antonyms": "Is this the opposite of ",
    "hyponyms": "Is this a kind of ",
    "meronyms": "Is this a part of ",
}

# Dictionary for sem_rel to amount of time on timer:
rel_time_map = {"synonyms": 10, "antonyms": 10, "hyponyms": 15, "meronyms": 20}


def index(request):
    context = dict()
    if request.user.is_authenticated():
        user_stat = utils.get_or_create_user_stat(request.user)
        context["rounds_played"] = user_stat.rounds_played
        context["total_score"] = round(user_stat.total_score, 2)
        if context["rounds_played"] <= 0:
            context["average_score"] = 0
        else:
            context["average_score"] = round(
                user_stat.total_score / user_stat.rounds_played, 2
            )
    return render(request, "welcome.html", context)


def models(request):
    word_relationship_formset = formset_factory(WordRelationshipForm, extra=1)
    if request.user.is_authenticated:
        user_stat = utils.get_or_create_user_stat(request.user)
        user_stat.last_login = date.today()
        user_stat.save()

    # We should select a relationship randomly from the set of selected ones. If none were selected,
    # just choose randomly for all (unless we want some javascript solution)
    if request.method == "POST":
        if "skip" in request.POST:
            if request.user.is_authenticated():
                utils.skip_word(request, conc_rating)
            return HttpResponse("Success")
        else:
            new_rels = request.POST.getlist("checks")
            request.session["relationships"] = new_rels
    rel_options = (
        request.session["relationships"]
        if request.session["relationships"]
        else ["meronyms", "antonyms", "hyponyms", "synonyms"]
    )
    sem_rel = random.choice(list([str(x) for x in rel_options]))

    # The question and list of base words are specific to the selected relationship type
    question = rel_q_map[sem_rel]
    vocab = vocabs[sem_rel]
    # 5% of the time pick a random unplayed word, otherwise dynamically select one based on user stats.
    if request.user.is_authenticated:
        vocab_index = utils.rel_index(sem_rel, user_stat)
        if random.random() >= 0.95 or len(vocab) < vocab_index:
            vocab_index = utils.random_select_unplayed_word(len(vocab), sem_rel)
            request.session["random_vocab"] = True
    else:
        vocab_index = utils.random_select_unplayed_word(len(vocab), sem_rel)
        request.session["random_vocab"] = True

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
        "time": rel_time_map[sem_rel],
    }
    return render(request, "input_words.html", context)


def scoring(request):
    # if this is a POST request, we need to process the form data
    if request.method == "POST":
        sem_rel = request.POST["sem_rel"]
        base_word = request.POST["base_word"]
        index = request.POST["word_index"]
        # If the user is authenticated, mark this word as played.
        if request.user.is_authenticated():
            utils.mark_played(request.user, index, base_word, sem_rel)

        num_forms_returned = int(request.POST["form-TOTAL_FORMS"])
        input_words = [
            (request.POST["form-%s-word" % i])[0:50] for i in range(num_forms_returned)
        ]
        context = {}
        # Creates scores based on the words and the semantic relationship
        context["base_word"] = base_word

        relations_percentages = utils.get_relations_percentages(sem_rel, base_word)
        context["percentages"] = {
            "data": [
                {"word": str(word), "percentage": pct}
                for word, pct in relations_percentages[:5]
            ]
        }
        # Now a list of tuples (word,dict), not a dictionary itself
        word_scores = utils.score_words(
            base_word, input_words, sem_rel, relations_percentages
        )
        context["word_scores"] = word_scores
        round_total = sum([scores["total_score"] for word, scores in word_scores])

        # If this word has been played less than 5 times, give the user a score bonus
        # 1 form returned means that no words were submitted
        word_stat = utils.get_or_create_word_stat(base_word, sem_rel, index)

        first_response_bonus = (
            40
            if word_stat.rounds_played <= 5
            and (num_forms_returned > 1 or input_words[0] != "")
            else 0
        )
        if request.user.is_authenticated():
            user_stat = utils.get_or_create_user_stat(request.user)
        context["first_response_bonus"] = first_response_bonus
        context["round_total"] = round_total + first_response_bonus

        user_inputs = UserInput.objects.filter(
            relation__type=sem_rel, relation__base_word=base_word
        )
        context["times_played"] = (
            user_inputs.values("user", "round_number").distinct().count()
        )
        answer = rel_a_map[sem_rel]

        answer = utils.add_det(answer, base_word, sem_rel, determiners)
        answer += base_word
        context["answer"] = answer

        # If the user is authenticated, store their data and the new word data.
        if request.user.is_authenticated():
            utils.store_round(sem_rel, base_word, index, word_scores, request)
        # Otherwise just store the word data.
        else:
            utils.anon_store_round(sem_rel, base_word, index, word_scores)
        return render(request, "scoring.html", context)
    else:
        return redirect("/models/")


def confirmation(request):
    word_relationship_formset = formset_factory(WordRelationshipForm)
    if request.method == "POST":
        new_rels = request.POST.getlist("checks")
        request.session["relationships"] = new_rels

    # We should select a relationship randomly from the set of selected ones. If none were selected,
    # just choose randomly for all
    rel_options = (
        request.session["relationships"]
        if request.session["relationships"]
        else ["meronyms", "antonyms", "hyponyms", "synonyms"]
    )
    sem_rel = random.choice(list([str(x) for x in rel_options]))

    vocab = vocabs[sem_rel]
    # Select a base word to play the word game on. Picks from words with at least 5 relations created by the normal word game.
    base_word = utils.find_base_word(vocab, sem_rel)

    phrase = rel_p_map[sem_rel]
    # Add the correct determiner to the word
    phrase = utils.add_det(phrase, base_word, sem_rel, determiners)

    # Find words to compare against base word. Mixture of relations and top words from the model.
    word_set = utils.find_word_pairs(base_word, sem_rel, {}, vocabs)
    context = {
        "title": "Know Your Nyms?",
        "formset": word_relationship_formset,
        "base_word": base_word,
        "sem_rel": sem_rel,
        "word_set": {"data": [{"word": str(word)} for word in word_set]},
        "curr_word": word_set[0],
        "phrase": phrase,
        "time": 20,
    }
    return render(request, "nymornot.html", context)


def confirmation_scoring(request):
    if request.method == "POST":
        word_set = request.POST["word_set"].split(",")

        results = (
            list()
            if request.POST["results"] == ""
            else [int(x) for x in request.POST["results"].split(",")]
        )

        sem_rel = request.POST["sem_rel"]
        base_word = request.POST["base_word"]

        context = dict()
        # Save result of the nym confirmation game.
        word_scores = utils.score_conf_words(sem_rel, base_word, word_set, results)
        round_total = 0
        for (a, b, c, score) in word_scores:
            round_total += score

        utils.save_conf_scores(word_set, results, sem_rel, base_word)
        context["word_scores"] = word_scores
        context["round_total"] = round_total

        answer = rel_a_map[sem_rel]
        answer = utils.add_det(answer, base_word, sem_rel, determiners)

        answer += base_word
        context["answer"] = answer

        return render(request, "nymornot_scoring.html", context)
    else:
        return redirect("/confirmation/")


def leaderboard(request):
    context = dict()
    rnds_played_set = UserStat.objects.order_by("-rounds_played")
    total_score_set = UserStat.objects.order_by("-total_score")
    word_score_set = WordStat.objects.order_by("avg_score")
    # Only words played 10+ times are allowed on the leaderboard
    word_score_list = list([x for x in word_score_set if x.rounds_played >= 10])

    average_score_list = list(UserStat.objects.all())
    # Only players who have played 10+ rounds are allowed on the leaderboard
    # Furthermore players who have not played in a month are not ranked for avg score.
    average_score_list = [x for x in average_score_list if x.rounds_played >= 10]
    average_score_list = [
        x for x in average_score_list if abs((date.today() - x.last_login).days) <= 30
    ]
    average_score_list.sort(
        key=lambda x: utils.div(x.total_score, x.rounds_played), reverse=True
    )

    # If the user is authenticated, gather data on them in addition to just top players
    if request.user.is_authenticated():
        user_stat = utils.get_or_create_user_stat(request.user)
        context["rounds_played"] = user_stat.rounds_played
        context["total_score"] = round(user_stat.total_score, 2)
        context["avg_score"] = round(
            utils.div(user_stat.total_score, user_stat.rounds_played), 2
        )
        rounds_played_rank = utils.rank(
            rnds_played_set,
            user_stat,
            lambda x: x.rounds_played,
            0,
            len(rnds_played_set) - 1,
        )
        total_score_rank = utils.rank(
            total_score_set,
            user_stat,
            lambda x: x.total_score,
            0,
            len(total_score_set) - 1,
        )
        avg_score_rank = utils.rank(
            average_score_list,
            user_stat,
            lambda x: utils.div(x.total_score, x.rounds_played),
            0,
            len(average_score_list) - 1,
        )
        context["total_score_rank"] = (
            str(total_score_rank + 1) if total_score_rank >= 0 else "-"
        )
        context["avg_score_rank"] = (
            str(avg_score_rank + 1) if avg_score_rank >= 0 else "-"
        )
        context["rounds_played_rank"] = (
            str(rounds_played_rank + 1) if rounds_played_rank >= 0 else "-"
        )
        context["num_players"] = len(total_score_set)
    # Adding top x scores per category to context
    for i in range(0, 5):
        if i < len(word_score_list):
            stat = word_score_list[i]
            context["word_rank" + str(i + 1)] = stat.word
            context["word_score" + str(i + 1)] = round(stat.avg_score, 2)
            context["sem_rel" + str(i + 1)] = (
                "Synonyms of "
                if stat.sem_rel == "synonyms"
                else "Antonyms of "
                if stat.sem_rel == "antonyms"
                else rel_a_map[stat.sem_rel] + utils.get_det(stat.word, determiners)
            )
    for i in range(0, 5):
        if i < len(rnds_played_set):
            stat = rnds_played_set[i]
            context["rnd_rank" + str(i + 1)] = stat.user.username
            context["rnd_score" + str(i + 1)] = stat.rounds_played
    for i in range(0, 5):
        if i < len(total_score_set):
            stat = total_score_set[i]
            context["ttl_rank" + str(i + 1)] = stat.user.username
            context["ttl_score" + str(i + 1)] = round(stat.total_score, 2)
    for i in range(0, 10):
        if i < len(average_score_list):
            stat = average_score_list[i]
            context["avg_rank" + str(i + 1)] = stat.user.username
            val = 0
            if stat.rounds_played != 0:
                val = stat.total_score / stat.rounds_played
            context["avg_score" + str(i + 1)] = round(val, 2)
    return render(request, "leaderboard.html", context)


def signin(request):
    if request.user.is_authenticated:
        return redirect("/")
    context = {"login_failed": False}
    if request.method == "GET":
        return render(request, "signin.html", context)
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            # Rerenders page with login failed message.
            context["login_failed"] = True
            return render(request, "signin.html", context)


def signout(request):
    logout(request)
    return redirect("/")


def signup(request):
    context = {"signup_failed": False, "user_form": UserForm()}
    if request.method == "GET":
        return render(request, "signup.html", context=context)
    if request.method == "POST":
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect("/")

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            context["signup_failed"] = True
            context["error"] = user_form.errors
            return render(request, "signup.html", context)
