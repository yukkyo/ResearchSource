#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import shelve

# MAX_DAT_FILES = 10
# MAX_DAT_FILES = 1926
MAX_DAT_FILES = 500
FILES_PER_SHELVE = 50

VideoCount = 0

# initialize tag dictionary
dic_file_name = "../../ResearchData/All_Tags"

for num in range(0,MAX_DAT_FILES/FILES_PER_SHELVE):
	shelve_file_name = "../../ResearchData/All_Datas/All_Data" + ("%04d" % (num * FILES_PER_SHELVE)) + "to" + ("%04d" % ((num + 1) * FILES_PER_SHELVE))
	dic1 = shelve.open(shelve_file_name)
	all_metatags = dic1["all_metatags"]
	dic1.close()
	dic2 = shelve.open(dic_file_name)
	tags_count = dic2["AllTagAndCount"]
	dic2.close()
	for metatag in all_metatags:
		for tag in metatag["tags"]:
			tags_count[tag] += 1
		VideoCount += 1
		if(VideoCount % 10000 == 0):
			print "End videos: " + str(VideoCount)
	print "open dic_shelve"
	dic2 = shelve.open(dic_file_name)
	dic2["AllTagAndCount"] = tags_count
	dic2.close()
	print "close dic_shelve"
	print "End shelve_file: " + shelve_file_name
	print "End videos: " + str(VideoCount)