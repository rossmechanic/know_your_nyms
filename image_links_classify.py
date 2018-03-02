import json
import os, sys

#os.path.join(sys.path[0] current path, up to KnowYourNyms folder, next layer is static
concreteness = open(os.path.join(sys.path[0], "static/original_concreteness_vocab.txt"), 'r')
#only want the first column
pictures = open(os.path.join(sys.path[0], "static/index.tsv"), 'r')

concreteness_set = [line.lower().strip() for line in concreteness]

# some lines do NOT have 2 elements - get rid of those lines
# tuple of words and file path
picture_word_set = [(line.split('\t')[0].lower(), line.split('\t')[1].strip()) if len(line.split('\t')) == 2 else None for line in pictures]

picset = set([picture_word[0] for picture_word in picture_word_set])

# 19873 unique common words
intersection = set(concreteness_set).intersection(picset)

# [ result for x in x_sq for y in y_sq]
# for x in x_sq
#	for y in y_sq
# 		result

# intersection_paths = [pic_word for pic_word in picture_word_set for common_word in intersection if common_word in set(pic_word[0])]
intersection_paths = list()
for word_link in picture_word_set:
	if word_link[0] in intersection and len(word_link) == 2:
		intersection_paths.append(word_link)

# 19988 - has some extra path
# print(len(intersection_paths))
# print(intersection_paths)

with open('paths.json', 'w') as outfile:
    json.dump(intersection_paths, outfile)

concreteness.close()
pictures.close()