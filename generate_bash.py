import json, time, socket
import os, sys, requests

string = "#!/bin/sh\n# OGS options at top of script\n#$ -wd /home1/y/yuqiwang/log_folder/\ncd ~\npython parse_images.py paths_"

for i in xrange(1,201):
	currString = str(i)
	currString += ".json\n"
	with open('bashscript_'+str(i)+'.sh', 'w') as outfile:
			outfile.write(string+currString)
			outfile.close()
