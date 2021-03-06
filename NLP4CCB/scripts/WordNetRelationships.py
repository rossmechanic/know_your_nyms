"""
This file allows you to access semantic relationships from WordNet.
Gets all meronyms from all noun synsets in WordNet.
Also has a method that filters word pairs if they are meronyms, according to WordNet.
"""
from nltk.corpus import wordnet as wn
from collections import defaultdict
import json


def get_synonyms(n=10000000):
    # All nouns, adjectives, and verbs
    synsets = (
        list(wn.all_synsets("n"))[:n]
        + list(wn.all_synsets("a"))[:n]
        + list(wn.all_synsets("v"))[:n]
    )
    all_synonyms = defaultdict(set)
    for synset in synsets:
        original_lemmas = [
            str(lemma.name()).replace("_", " ") for lemma in synset.lemmas()
        ]
        for original_lemma in original_lemmas:
            all_synonyms[original_lemma] = all_synonyms[original_lemma].union(
                set(original_lemmas)
            )
    # Make the sets lists, so it can be turned into JSON
    all_synonyms = {
        str(k).lower(): list([str(m).lower() for m in v])
        for k, v in list(all_synonyms.items())
        if list(v)
    }
    return all_synonyms


def get_antonyms(n=10000000):
    # All nouns, adjectives, and verbs
    synsets = (
        list(wn.all_synsets("n"))[:n]
        + list(wn.all_synsets("a"))[:n]
        + list(wn.all_synsets("v"))[:n]
    )
    all_antonyms = defaultdict(set)
    for synset in synsets:
        original_lemmas = synset.lemmas()
        for original_lemma in original_lemmas:
            original_word = str(original_lemma.name()).replace("_", " ")
            antonym_lemmas = original_lemma.antonyms()
            antonym_words = [
                str(lemma.name()).replace("_", " ") for lemma in antonym_lemmas
            ]
            all_antonyms[original_word] = all_antonyms[original_word].union(
                set(antonym_words)
            )
    # Make the sets lists, so it can be turned into JSON
    all_antonyms = {
        str(k).lower(): list([str(m).lower() for m in v])
        for k, v in list(all_antonyms.items())
        if list(v)
    }
    return all_antonyms


# Returns a dictionary that maps all words to a list of their meronyms.
def get_meronyms(n=10000000, holonyms=False):
    synsets = list(wn.all_synsets("n"))[:n]  # All noun synsets
    all_meronyms = defaultdict(set)
    for synset in synsets:
        # All meronyms for this synset
        meronym_synsets = (
            synset.member_meronyms()
            + synset.substance_meronyms()
            + synset.part_meronyms()
        )
        # In the case that we are doing holonyms
        if holonyms:
            meronym_synsets = (
                synset.member_holonyms()
                + synset.substance_holonyms()
                + synset.part_holonyms()
            )
        if meronym_synsets:
            # Go through all lemmas from the original synset
            original_lemmas = [
                str(lemma.name()).replace("_", " ") for lemma in synset.lemmas()
            ]
            for original_lemma in original_lemmas:
                # Go through all meronym synsets for that original synset
                for meronym_synset in meronym_synsets:
                    # Gather all lemmas for the meronym synset
                    meronym_lemmas = [
                        str(lemma.name()).replace("_", " ")
                        for lemma in meronym_synset.lemmas()
                    ]
                    # Add them to the meronym set for the lemma
                    all_meronyms[original_lemma] = all_meronyms[original_lemma].union(
                        set(meronym_lemmas)
                    )
    # Make the sets lists, so it can be turned into JSON
    all_meronyms = {
        str(k).lower(): list([str(m).lower() for m in v])
        for k, v in list(all_meronyms.items())
        if list(v)
    }
    return all_meronyms


def get_hyponyms(n=10000000, hypernyms=False):
    synsets = list(wn.all_synsets("n"))[:n]  # All noun synsets
    all_hyponyms = defaultdict(set)
    for synset in synsets:
        # All meronyms for this synset
        hyponym_synsets = synset.hyponyms()
        # In the case that we are doing holonyms
        if hypernyms:
            hyponym_synsets = synset.hypernyms()
        if hyponym_synsets:
            # Go through all lemmas from the original synset
            original_lemmas = [
                str(lemma.name()).replace("_", " ") for lemma in synset.lemmas()
            ]
            for original_lemma in original_lemmas:
                # Go through all hyponym synsets for that original synset
                for hyponym_synset in hyponym_synsets:
                    # Gather all lemmas for the meronym synset
                    hyponym_lemmas = [
                        str(lemma.name()).replace("_", " ")
                        for lemma in hyponym_synset.lemmas()
                    ]
                    # Add them to the meronym set for the lemma
                    all_hyponyms[original_lemma] = all_hyponyms[original_lemma].union(
                        set(hyponym_lemmas)
                    )
    # Make the sets lists, so it can be turned into JSON
    all_hyponyms = {
        str(k).lower(): list([str(m).lower() for m in v])
        for k, v in list(all_hyponyms.items())
        if list(v)
    }
    return all_hyponyms


# Returns only the pairs that appear in WordNet (that are confirmed meronyms)
def find_meronyms(pairs):
    all_meronyms = get_meronyms()
    actual_meronyms = [
        pair
        for pair in pairs
        if pair[0] in all_meronyms and pair[1] in all_meronyms[pair[0]]
    ]
    return actual_meronyms


def get_meronym_tree(string, meronyms):
    dic = {"name": string}

    ms = meronyms[string]

    if ms:
        children = []
        for mer in ms:
            children.append(get_meronym_tree(mer, meronyms))
        dic["children"] = children
    return dic


def create_json(d, filepath):
    json.dump(d, open(filepath, "w"))


def create_meronym_json(string, filepath):
    meronyms = get_meronyms()

    tree = get_meronym_tree(string, meronyms)

    json.dump(tree, open(filepath, "w"))


# d = get_antonyms()
# create_json(d, 'wordnet_antonyms.json')
