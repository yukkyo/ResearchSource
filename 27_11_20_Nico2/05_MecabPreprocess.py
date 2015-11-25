#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MeCab
import shelve
import cPickle

# Mecabを用いて1100000文書に対して形態素解析を行う

MAX_SHELVE_FILES = 11
FILES_PER_SHELVE = 50

shelve_file_path = "../../ResearchData/All_Datas/All_Data"
after_mecab_file = "../../ResearchData/Experiment2/after_mecab/after_mecab"

my_tagger = MeCab.Tagger('-Owakati -u ../../ResearchData/Experiment2/nico.dic')

VideoCount = 0
after_mecab_docs = []
append = after_mecab_docs.append

for num in range(0, MAX_SHELVE_FILES):
	file_name = shelve_file_path + ("%04d" % (num * FILES_PER_SHELVE)) + "to" + ("%04d" % ((num + 1) * FILES_PER_SHELVE))
	print "open: " + file_name
	dic1 = shelve.open(file_name)
	all_metatags = dic1["all_metatags"]
	dic1.close()

	# after_mecab_docs = []
	# append = after_mecab_docs.append

	for metatag in all_metatags:
		after_mecab = ["___" + tag for tag in metatag["tags"]]
		after_mecab.extend(my_tagger.parse(metatag["title"]).split(" "))
		after_mecab.extend(my_tagger.parse(metatag["description"]).split(" "))
		append(after_mecab)
		VideoCount += 1
		if(VideoCount % 10000 == 0):
			print "End videos: " + str(VideoCount)
			if(VideoCount == 1100000):
				print "break because videocount is 1100000"
				break
	all_metatags = None

	# with open(after_mecab_file + str(num) + '.pkl', "wb") as f:
	# 	print "open for saving: " + after_mecab_file
	# 	cPickle.dump(after_mecab_docs, f, cPickle.HIGHEST_PROTOCOL)
	# 	print "saving is end"

	if (VideoCount == 1100000):
		print "break again because videocount is 1100000"
		break

	print "End videos: " + str(VideoCount)

with open(after_mecab_file + '1.pkl', "wb") as f:
	print "open for saving: " + after_mecab_file + '1.pkl'
	cPickle.dump(after_mecab_docs[0:500000], f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"

with open(after_mecab_file + '2.pkl', "wb") as f:
	print "open for saving: " + after_mecab_file + '2.pkl'
	cPickle.dump(after_mecab_docs[500000:1000000], f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"

with open(after_mecab_file + '_test.pkl', "wb") as f:
	print "open for saving: " + after_mecab_file + '_test.pkl'
	cPickle.dump(after_mecab_docs[1000000:1100000], f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"