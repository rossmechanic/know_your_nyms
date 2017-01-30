import json
import os
from NLP4CCB_Django_App import settings


def get_data_from_rels(rels):
	# hardcoding this for now. Will need to change this when we deploy (but also won't have a json we access when we
	# deploy)
	data = json.load(open(os.path.join(settings.STATIC_ROOT, 'data/result_ltw.json')))

	mer_pairs = data.keys()

	filtered_data = []

	for i, rel in enumerate(rels):
		dic = {}
		if '\t'.join(rel) in mer_pairs:
			dic["word1"] = rel[0]
			dic["word2"] = rel[1]
			rel_data = data['\t'.join(rel)]
			l = []
			for i, sentence in enumerate(rel_data['S']):
				l.append((sentence, rel_data['POS'][i]))
			dic["S"] = l

		elif '\t'.join(tuple(reversed(rel))) in mer_pairs:
			dic["word1"] = rel[1]
			dic["word2"] = rel[0]
			rel_data = data['\t'.join(tuple(reversed(rel)))]
			l = []
			for i, sentence in enumerate(rel_data['S']):
				l.append((sentence, rel_data['POS'][i]))
			dic["S"] = l
		else:
			#pair of words has no common sentences
			print "No words returned for the pair: ", rel
			continue
		filtered_data.append(dic)
	return filtered_data
