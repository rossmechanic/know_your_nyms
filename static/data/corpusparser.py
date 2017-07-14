import sets
import re

meronyms = sets.Set()
vocab_file = '/Users/jacbrad/Documents/Research/NLP4CCB_Django_App/static/data/model_top_words.txt'
pat = re.compile(r'(?P<base_word>[0-9a-zA-Z ]+)\t(?P<sem_rel>(meronyms|hyponyms|synonyms|antonyms))\t(?P<word>[0-9a-zA-Z ]+)\t(?P<score>0.[0-9]+)$')
with open(vocab_file) as f:
	lines = f.readlines()
for line in lines:
	res = pat.match(line)
	if res:
		if not (res.group('base_word') in meronyms):
			meronyms.add(res.group('base_word'))

print("added meronyms")

hyponyms = sets.Set()
'''
vocab_file = '/Users/jacbrad/Documents/Research/NLP4CCB_Django_App/static/data/hyponyms_base_words.txt'
with open(vocab_file) as f:
	lines = f.readlines()
for x in lines:
	hyponyms.add(x.lower().strip())'''


print("added hyponyms")

print("preparing to read the corpus")
determiners = dict()

pat = re.compile(r'of (((?P<det>a|an|the) (?P<word1>(\S+)) (?P<word2>(\S+)))|(?P<word3>(\S+)) (?P<word4>(\S+)) \S+)\t(?P<count>([0-9])+)$')

for line in open('/Users/jacbrad/Documents/4gms/corpus'):
	res = pat.match(line)
	if res:
		det = ''
		word1 = ''
		word2 = ''
		if res.group('det'):
			det = res.group('det')
			word1 = res.group('word1')
			word2 = res.group('word2')
		else:
			word1 = res.group('word3')
			word2 = res.group('word4')
		combined_word = word1 + ' ' + word2
		count = res.group('count')
		if word1 != 'some':
			if word1 in meronyms or word1 in hyponyms:
				if not ((word1,det) in determiners):
					determiners[(word1,det)] = 0.0
				determiners[(word1,det)] = determiners[(word1,det)] + int(count)

			if combined_word in meronyms or combined_word in hyponyms:
				if not ((combined_word,det) in determiners):
					determiners[(combined_word,det)] = 0.0
				determiners[(combined_word,det)] = determiners[(combined_word,det)] + int(count)
print("Done reading, now writing to files")

with open('/Users/jacbrad/Documents/conf_determiners.txt', 'w') as f:
	for word in meronyms.union(hyponyms):
		for d in ['a', 'an', '', 'the']:
			if (word,d) in determiners:
				f.write(word + "=" + d + "=" + str(determiners[(word,d)]) + "\n")


