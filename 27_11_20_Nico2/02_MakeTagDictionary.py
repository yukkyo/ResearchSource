#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 全ての文書

import json
import shelve
import cPickle

# MAX_DAT_FILES = 10
# MAX_DAT_FILES = 1926
MAX_DAT_FILES = 600
FILES_PER_SHELVE = 50

VideoCount = 0 

file_name_all_tags = "../../ResearchData/Experiment2/all_tags.pkl"
# initialize tag dictionary
tag_set = set([])

for num in range(0,MAX_DAT_FILES/FILES_PER_SHELVE):
	shelve_file_name = "../../ResearchData/All_Datas/All_Data" + ("%04d" % (num * FILES_PER_SHELVE)) + "to" + ("%04d" % ((num + 1) * FILES_PER_SHELVE))
	print "open: " + shelve_file_name
	dic1 = shelve.open(shelve_file_name)
	all_metatags = dic1["all_metatags"]
	dic1.close()
	for metatag in all_metatags:
		for tag in metatag["tags"]:
			tag_set.add(tag)
		VideoCount += 1
		if(VideoCount % 10000 == 0):
			print "End videos: " + str(VideoCount)
			if VideoCount == 1000000:
				print "break because videocount is 1,000,000"
				break
	if VideoCount == 1000000:
		print "break again because videocount is 1,000,000"
		break
print "len(tag_set): " + str(len(tag_set))

with open(file_name_all_tags, "wb") as f:
	print "saveing: " + file_name_all_tags
	cPickle.dump(tag_set, f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"