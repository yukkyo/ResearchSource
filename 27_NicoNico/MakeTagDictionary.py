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
tag_dic = shelve.open(dic_file_name)
tag_dic["all_tag_dictionary"] = set([])
tag_dic.close()

for num in range(0,MAX_DAT_FILES/FILES_PER_SHELVE):
	shelve_file_name = "../../ResearchData/All_Datas/All_Data" + ("%04d" % (num * FILES_PER_SHELVE)) + "to" + ("%04d" % ((num + 1) * FILES_PER_SHELVE))
	dic1 = shelve.open(shelve_file_name)
	all_metatags = dic1["all_metatags"]
	dic1.close()
	tag_dictionary = set([])
	for metatag in all_metatags:
		for tag in metatag["tags"]:
			tag_dictionary.add(tag)
		VideoCount += 1
		if(VideoCount % 10000 == 0):
			print "End videos: " + str(VideoCount)
	print "open dic_shelve"
	dic2 = shelve.open(dic_file_name)
	all_tag_dictionary = dic2["all_tag_dictionary"]
	dic2["all_tag_dictionary"] = all_tag_dictionary.union(tag_dictionary)
	dic2.close()
	print "close dic_shelve"
	print "End shelve_file: " + shelve_file_name
	print "End videos: " + str(VideoCount)

# all_metatags = []
# START_DAT_FILES = MAX_DAT_FILES - MAX_DAT_FILES % FILES_PER_SHELVE

# for i in range(START_DAT_FILES, MAX_DAT_FILES):
# 	print i

# shelve_file_name = "../../ResearchData/All_Data" + ("%04d" % (START_DAT_FILES)) + "to" + ("%04d" % (MAX_DAT_FILES))
# dic2 = shelve.open(shelve_file_name)
# dic2["all_metatags"] = all_metatags
# dic2.close()
# print "End shelve_file: " + shelve_file_name
# print "End videos: " + str(VideoCount)