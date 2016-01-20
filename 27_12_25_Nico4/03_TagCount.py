#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shelve
import cPickle

MAX_DAT_FILES = 600
FILES_PER_SHELVE = 50
MAX_VIDEO_COUNT = 1000000

VideoCount = 0
file_name_all_tags = "../../ResearchData/Experiment4/all_tags.pkl"
f_tag_count_dic = "../../ResearchData/Experiment4/tag_count_dic.pkl"

# initialize tag count dictionary
tag_count_dic = None
with open(file_name_all_tags, 'rb') as f:
	print "open: " + file_name_all_tags
	all_tags = cPickle.load(f)
	tag_count_dic = dict( zip( all_tags, [0] * len(all_tags) ) )
	print "made tag_count_dic, len(tag_count_dic): " + str(len(tag_count_dic))

for num in range(0,MAX_DAT_FILES/FILES_PER_SHELVE):
	shelve_file_name = "../../ResearchData/All_Datas/All_Data" + ("%04d" % (num * FILES_PER_SHELVE)) + "to" + ("%04d" % ((num + 1) * FILES_PER_SHELVE))
	dic1 = shelve.open(shelve_file_name)
	all_metatags = dic1["all_metatags"]
	dic1.close()
	for metatag in all_metatags:
		for tag in metatag["tags"]:
			tag_count_dic[tag] += 1
		VideoCount += 1
		if(VideoCount % 10000 == 0):
			print "End videos: " + str(VideoCount)
			if VideoCount == MAX_VIDEO_COUNT:
				print "break because videocount is 1000000"
				break
	if VideoCount == MAX_VIDEO_COUNT:
		print "break again"
		break

with open(f_tag_count_dic, 'wb') as f:
	print "open for saving: " + f_tag_count_dic
	cPickle.dump(tag_count_dic, f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"
