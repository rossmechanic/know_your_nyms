import os
import re

from django.core.management import BaseCommand

import settings
import json

BASE_STATIC_DIR = os.path.join(settings.BASE_DIR, "NLP4CCB/static")


class Command(BaseCommand):
    help = "Generates mapping json files to be used in views.py"

    def handle(self, *args, **options):
        # Read in the vocabulary to traverse
        relationships = ["synonyms", "antonyms", "hyponyms", "meronyms"]
        vocabs = {}
        for rel in relationships:
            vocab_file = "original_{rel}_vocab.txt".format(rel=rel)
            with open(os.path.join(BASE_STATIC_DIR, vocab_file)) as f:
                lines = f.readlines()
            vocabs[rel] = [word.lower().strip() for word in lines]

        with open(os.path.join(BASE_STATIC_DIR, "rel_to_vocab_map.json"), "w") as f:
            json.dump(vocabs, f)

        # Set up a map from words to their determiners, a/an/the/etc
        determiners = dict()
        pat = re.compile(r"(?P<word>[0-9a-zA-Z ]+)=(?P<det>\S*)$")
        det_rels = ["meronyms", "hyponyms"]
        for rel in det_rels:
            det_file = rel + "_determiners.txt"
            for line in open(os.path.join(BASE_STATIC_DIR, det_file)):
                res = pat.match(line)
                if res:
                    p = res.group("det")
                    word = res.group("word")
                    if p == "":
                        determiners[word] = p
                    else:
                        determiners[word] = p + " "
        with open(os.path.join(BASE_STATIC_DIR, "determiner_map.json"), "w") as f:
            json.dump(determiners, f)

        # Map from words to their index.
        ind = dict()
        for rel in relationships:
            for i in range(0, len(vocabs[rel])):
                ind[vocabs[rel][i], rel] = i

        # Find the top 100 words predicted by the model for each base word in the concreteness data set.
        conc_rating = dict()
        conc_file = "concreteness_ratings.txt"
        ignorefirst = True
        for line in open(os.path.join(BASE_STATIC_DIR, conc_file)):
            if not ignorefirst:
                words = line.split("\t")
                base_word = words[0]
                conc_mean = float(words[2])
                percent_known = float(words[6])
                in_base_words = False
                for rel in relationships:
                    if (base_word, rel) in ind and not in_base_words:
                        conc_rating[base_word] = (conc_mean, percent_known)
                        in_base_words = True
            else:
                ignorefirst = False

        with open(os.path.join(BASE_STATIC_DIR, "concreteness_rating.json"), "w") as f:
            json.dump(conc_rating, f)
