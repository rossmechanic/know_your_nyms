import sets
import re

def arg_max1(dic, word):
	pronouns = ['a', '', 'an']
	argmax = 'a'
	countmax = 0
	print(word)
	for p in pronouns:
		if (word,p) in dic:
			if p == '':
				dic[(word,p)] = dic[(word,p)]//25
			if dic[(word,p)] > countmax:
				countmax = dic[(word,p)]
				argmax = p

	print(argmax)
	return argmax

meronyms = sets.Set()
vocab_file = '/Users/jacbrad/Documents/Research/NLP4CCB_Django_App/static/data/model_top_words.txt'
pat = re.compile(r'(?P<base_word>[0-9a-zA-Z ]+)\t(?P<sem_rel>(meronyms|hyponyms|synonyms|antonyms))\t(?P<word>[0-9a-zA-Z ]+)\t(?P<score>0.[0-9]+)$')
with open(vocab_file) as f:
	lines = f.readlines()
for line in lines:
	res = pat.match(line)
	if res:
		meronyms.add(res.group('base_word'))

print("added hyponyms")

print("preparing to read the corpus")
pronouns = dict()

pat = re.compile(r'of (((?P<pronoun>a|an) (?P<word1>(\S+)) (?P<word2>(\S+)))|(?P<word3>(\S+)) (?P<word4>(\S+)) \S+)\t(?P<count>([0-9])+)$')

for line in open('/Users/jacbrad/Documents/4gms/corpus'):
	res = pat.match(line)
	if res:
		pronoun = ''
		word1 = ''
		word2 = ''
		if res.group('pronoun'):
			pronoun = res.group('pronoun')
			word1 = res.group('word1')
			word2 = res.group('word2')
		else:
			word1 = res.group('word3')
			word2 = res.group('word4')
		combined_word = word1 + ' ' + word2
		count = res.group('count')
		if word1 != 'the' and word1 != 'some':
			if word1 in meronyms:
				if not ((word1,pronoun) in pronouns):
					pronouns[(word1,pronoun)] = 0
				pronouns[(word1,pronoun)] = pronouns[(word1,pronoun)] + 1

			if combined_word in meronyms:
				if not ((combined_word,pronoun) in pronouns):
					pronouns[(combined_word,pronoun)] = 0
				pronouns[(combined_word,pronoun)] = pronouns[(combined_word,pronoun)] + 1
print("Done reading, now writing to files")

with open('/Users/jacbrad/Documents/Research/NLP4CCB_Django_App/static/data/meronyms_determiners.txt', 'w') as f:
	for word in meronyms:
		f.write(word + "=" + arg_max1(pronouns, word) + "\n")
