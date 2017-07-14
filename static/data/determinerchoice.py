import sets
import re

def starts_with_vowel(word):
	vowels = ['A', 'E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u']
	return word[0] in vowels
def arg_second_max(dic, word):
	determiners = dict()
	determiners['a'] = 0
	determiners[''] = 0
	determiners['an'] = 0
	determiners['the'] = 0

	for d in determiners:
		if (word,d) in dic:
			determiners[d] = dic[(word,d)]
	amax = 'a'
	cmax = 0
	for d in determiners:
		if determiners[d] > cmax:
			cmax = determiners[d]
			amax = d
	del determiners[amax]
	amax = 'a'
	cmax = 0
	for d in determiners:
		if determiners[d] > cmax:
			cmax = determiners[d]
			amax = d
	if cmax == 0:
		return 'x'
	else:
		return amax

def arg_max(dic, word):
	determiners = ['a', '', 'an','the']
	countmax = 0
	dsum = 0
	factor = 0.7
	for d in determiners:
		if (word,d) in dic:
			dsum += dic[(word,d)]
	#Cutoff factor obtained through testing
	for d in determiners:
		if (word,d) in dic:
			if dic[(word,d)] >= factor*dsum and d != 'the':
				return d

	asm = arg_second_max(dic, word)
	if asm == '':
		if dic[(word,asm)] > .4*dsum:
			return ''
		else:
			if starts_with_vowel(word):
				det = 'an'
			else:
				det = 'a'
			maind = [det, 'the']

			if (word,maind[0]) in dic and (word, maind[1]) in dic:
				if dic[(word,maind[1])] >= 90*dic[(word,maind[0])]:
					return maind[1]
				else:
					return maind[0]
			elif (word,maind[0]) in dic:
				return maind[0]
			elif(word,maind[1] in dic):
				return maind[1]
			else:
				return 'a'
	else:
		if starts_with_vowel(word):
			det = 'an'
		else:
			det = 'a'
		maind = [det, 'the']

		if (word,maind[0]) in dic and (word, maind[1]) in dic:
			if dic[(word,maind[1])] >= 90*dic[(word,maind[0])]:
				return maind[1]
			else:
				return maind[0]
		elif (word,maind[0]) in dic:
			return maind[0]
		elif(word,maind[1] in dic):
			return maind[1]
		else:
			return 'a'

def hyp_arg_max(dic, word):
	determiners = ['a', '', 'an']
	countmax = 0
	dsum = 0
	factor = 0.7
	for d in determiners:
		if (word,d) in dic:
			dsum += dic[(word,d)]
	#Cutoff factor obtained through testing
	for d in determiners:
		if (word,d) in dic:
			if dic[(word,d)] >= factor*dsum:
				return d
	return ' '

meronyms = sets.Set()
vocab_file = '/Users/jacbrad/Documents/Research/NLP4CCB_Django_App/static/data/meronyms_base_words.txt'
with open(vocab_file) as f:
	lines = f.readlines()
for x in lines:
	meronyms.add(x.lower().strip())

print("added meronyms")

hyponyms = sets.Set()
vocab_file = '/Users/jacbrad/Documents/Research/NLP4CCB_Django_App/static/data/hyponyms_base_words.txt'
with open(vocab_file) as f:
	lines = f.readlines()
for x in lines:
	hyponyms.add(x.lower().strip())

determiners = dict()
pat = re.compile(r'(?P<word>[0-9a-zA-Z ]+)=(?P<det>\S*)=(?P<count>\S+)$')
for line in open('/Users/jacbrad/Documents/determiners.txt'):
	res = pat.match(line)
	if res:
		w = res.group('word')
		print(w + " " + res.group('det') + " " + res.group('count'))
		determiners[(w, res.group('det'))] = float(res.group('count'))

print("loaded from file")

with open('/Users/jacbrad/Documents/Research/NLP4CCB_Django_App/static/data/meronyms_determiners.txt', 'w') as f:
	for word in meronyms:
		f.write(word + "=" + arg_max(determiners, word) + "\n")
with open('/Users/jacbrad/Documents/Research/NLP4CCB_Django_App/static/data/hyponyms_determiners.txt', 'w') as f:
	for word in hyponyms:
		f.write(word + "=" + hyp_arg_max(determiners, word) + "\n")


