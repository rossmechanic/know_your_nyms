import json
import re

wn_syn = json.load(open('wordnet_synonyms.json'))
wn_ant = json.load(open('wordnet_antonyms.json'))
wn_hyp = json.load(open('wordnet_hyponyms.json'))
wn_mer = json.load(open('wordnet_meronyms.json'))

print ('Number WN Synonyms: ', len(wn_syn))
print ('Number WN Antonyms: ', len(wn_ant))
print ('Number WN Hyponyms: ', len(wn_hyp))
print ('Number WN Meronyms: ', len(wn_mer))
print '\n'

def create_dict(rel):
    with open(rel + '_base_words.txt-counts') as f:
        d = {}
        for line in f.readlines():
            s = line.strip().split('\t')
            k = s[0].strip()
            v = int(s[1])
            d[k] = v
        print ('Original ' + rel + ' Length: ', len(d))
        d = {k:v for k,v in d.items() if d[k] >= 1000000}
        print ('Filtered by 1000000 ' + rel + ' Length: ', len(d))
        return d

syn_d = create_dict('synonyms')
ant_d = create_dict('antonyms')
hyp_d = create_dict('hyponyms')
mer_d = create_dict('meronyms')


synonyms = [word for word in syn_d if len(word) > 2]
antonyms = [word for word in ant_d if len(word) > 2]
hyponyms = [word for word in hyp_d if len(word) > 2]
meronyms = [word for word in mer_d if len(word) > 2]

print ('Number of Synonym Words: ', len(synonyms))
print ('Number of Antonym Words: ', len(antonyms))
print ('Number of Hyponym Words: ', len(hyponyms))
print ('Number of Meronym Words: ', len(meronyms))

for (rel, words) in [('synonyms', synonyms), ('antonyms', antonyms), ('hyponyms', hyponyms), ('meronyms', meronyms)]:
    with open(rel + '_base_words.txt', 'w') as f:
        for word in words:
            f.write(word + '\n')