#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import shelve

# MAX_DAT_FILES = 10
MAX_DAT_FILES = 1926
# MAX_DAT_FILES = 30
FILES_PER_SHELVE = 50

VideoCount = 0
for num in range(0,MAX_DAT_FILES/FILES_PER_SHELVE):
	all_metatags = []
	for i in range(FILES_PER_SHELVE):
		file_name = "../../ResearchData/Nico_Meta/" + ("%04d" % (num*FILES_PER_SHELVE + i)) + ".dat"
		with open(file_name, "r") as raw_files:
			for raw_file in raw_files:
				json_file = json.loads(raw_file)
				if(len(json_file["description"]) > 20):
					metatag = {}
					metatag["video_id"] = json_file["video_id"].encode("utf-8")
					metatag["title"] = json_file["title"].encode("utf-8")
					metatag["upload_time"] = json_file["upload_time"].encode("utf-8")
					metatag["description"] = json_file["description"].encode("utf-8")

					metatag_tags = []
					for tag in json_file["tags"]:
						metatag_tags.append(tag[u'tag'].encode("utf-8"))

					metatag["tags"] = metatag_tags
					all_metatags.append(metatag)
					VideoCount += 1
		print "DatFile end: " + ("%04d" % (num*FILES_PER_SHELVE + i))

	shelve_file_name = "../../ResearchData/All_Data" + ("%04d" % (num * FILES_PER_SHELVE)) + "to" + ("%04d" % ((num + 1) * FILES_PER_SHELVE))
	dic = shelve.open(shelve_file_name)
	dic["all_metatags"] = all_metatags
	dic.close()
	print "End shelve_file: " + shelve_file_name
	print "End videos: " + str(VideoCount)

all_metatags = []
START_DAT_FILES = MAX_DAT_FILES - MAX_DAT_FILES % FILES_PER_SHELVE

for i in range(START_DAT_FILES, MAX_DAT_FILES):
	file_name = "../../ResearchData/Nico_Meta/" + ("%04d" % (i)) + ".dat"
	with open(file_name, "r") as raw_files:
		for raw_file in raw_files:
			json_file = json.loads(raw_file)
			if(len(json_file["description"]) > 20):
				metatag = {}
				metatag["video_id"] = json_file["video_id"].encode("utf-8")
				metatag["title"] = json_file["title"].encode("utf-8")
				metatag["upload_time"] = json_file["upload_time"].encode("utf-8")
				metatag["description"] = json_file["description"].encode("utf-8")
				metatag_tags = []
				for tag in json_file["tags"]:
					metatag_tags.append(tag[u'tag'].encode("utf-8"))
				metatag["tags"] = metatag_tags
				all_metatags.append(metatag)
				VideoCount += 1
shelve_file_name = "../../ResearchData/All_Data" + ("%04d" % (START_DAT_FILES)) + "to" + ("%04d" % (MAX_DAT_FILES))
dic2 = shelve.open(shelve_file_name)
dic2["all_metatags"] = all_metatags
dic2.close()
print "End shelve_file: " + shelve_file_name
print "End videos: " + str(VideoCount)