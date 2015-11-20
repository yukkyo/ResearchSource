#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MeCab
import shelve
import cPickle

# Mecabを用いて1000000文書に対して形態素解析を行う

MAX_SHELVE_FILES = 10
# MAX_SHELVE_FILES = 1
FILES_PER_SHELVE = 50

VideoCount = 0
dic_file_name = "../../ResearchData/All_Tags"
shelve_file_path = "../../ResearchData/All_Datas/All_Data"
after_mecab_file = "../../ResearchData/After_Mecab/after_mecab"

my_tagger = MeCab.Tagger('-Owakati -u nico.dic')

for num in range(0, MAX_SHELVE_FILES):
	# shelve file open
	file_name = shelve_file_path + ("%04d" % (num * FILES_PER_SHELVE)) + "to" + ("%04d" % ((num + 1) * FILES_PER_SHELVE))
	dic1 = shelve.open(file_name)
	all_metatags = dic1["all_metatags"]
	dic1.close()
	after_mecabs = []
	append = after_mecabs.append
	# make each document per a video
	for metatag in all_metatags:
		after_mecab = ["___" + tag for tag in metatag["tags"]]
		after_mecab.extend(my_tagger.parse(metatag["title"]).split(" "))
		after_mecab.extend(my_tagger.parse(metatag["description"]).split(" "))
		append(after_mecab)
		VideoCount += 1
		if(VideoCount % 10000 == 0):
			print "End videos: " + str(VideoCount)
	all_metatags = None
	# print "open dic_shelve for save"
	# dic2 = shelve.open(after_mecab_file + str(num))
	# dic2["AfterMecab"] = after_mecabs
	# dic2.close()
	with open(after_mecab_file + str(num) + '.pkl', 'wb') as f:
		print "open pickle file for save"
		cPickle.dump(after_mecabs, f, cPickle.HIGHEST_PROTOCOL)
	after_mecabs = None
	print "close save_file"
	# print "End shelve_file: " + after_mecab_file + str(num)
	print "End file: " + after_mecab_file + str(num) + '.pkl'
	print "End videos: " + str(VideoCount)