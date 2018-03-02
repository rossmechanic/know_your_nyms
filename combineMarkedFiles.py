import json
import os, sys

final_string = ""
count = 0

for i in xrange(1, 201):
	f = open("/Users/carrie/Documents/Senior_Fall_2017/CIS 400/know_your_nyms/image_marked/markedImageLinks_paths_"+str(i)+".json", 'r')
	for l in f:
		lines = json.loads(l).split('\n')
		for line in lines:
			currLine = line.rstrip('~')
			word_pics = currLine.split('\t')
			if len(word_pics) == 2:
				final_string += word_pics[0].encode('utf-8')
				final_string += "\t"
				final_string += word_pics[1].encode('utf-8')
				final_string += "\n"


with open("picture_vocabs.txt", "w") as text_file:
	text_file.write(final_string)