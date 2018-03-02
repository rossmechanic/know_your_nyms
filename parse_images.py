import json, time, socket
import os, sys, requests

image_path = open(os.path.join(sys.path[0], "dummy_paths.json"), 'r')

string = ""

# Format: WORD \t link1 D,link2 A,etc
# every new line contains an extra , at the end
# can strip this before parsing by , or after

for line in image_path:
	allpaths = json.loads(line)
	for word, path in allpaths:
		string += word
		string += '\t'

		# probably need to put the share the stuff before path when you load it
		f = open(os.path.join(sys.path[0], "/scratch-shared/users/bcal/packages/"+path+"metadata.json"), 'r')
		for l in f:
			json_file = json.loads(l)
			for item in json_file:
				image_link = json_file[item]["image_link"]
				string += json_file[item]["image_link"]
				try:
					request = requests.get(image_link)
				except:
					pass
				else:
					if request.status_code == 200:
						string += " A"
					else:
						string += " D"
				string += ","
		f.close()
		string += "\n"

image_path.close()
with open('markedImageLinks.json', 'w') as outfile:
    json.dump(string, outfile)