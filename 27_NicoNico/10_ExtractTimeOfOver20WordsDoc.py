#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shelve
import cPickle

# 20語未満の文書を取り除く

MAX_SHELVE_FILES = 6
FILES_PER_SHELVE = 50
MAX_PICKLE_FILES = 6

shelve_file_path = "../../ResearchData/All_Datas/All_Data"
after_remove_file = "../../ResearchData/After_Remove/after_remove_stop_word"
extracted_times_file = "../../ResearchData/After_Extract_Over20Words/times_of_over20words.pkl"
all_times = []
extracted_times = []

# 前処理をする前の文書から
for num in range(0, MAX_SHELVE_FILES):
	# shelve file open
	file_name = shelve_file_path + ("%04d" % (num * FILES_PER_SHELVE)) + "to" + ("%04d" % ((num + 1) * FILES_PER_SHELVE))
	print "shelve file open:" + str(num)
	dic1 = shelve.open(file_name)
	all_metatags = dic1["all_metatags"]
	dic1.close()
	# make each document per a video
	all_times.extend([metatag["upload_time"] for metatag in all_metatags])
	print "end all_times: " + str(len(all_times))

# 記号をとった文書から
for num in range(0, MAX_PICKLE_FILES):
	with open(after_remove_file + str(num) + '.pkl', 'rb') as f:
		docs = cPickle.load(f)
		print "len(after_remove_docs) :" + str(len(docs))
		# 各文書から20語以上の文書の時間をとってくる
		extracted_times.extend([all_times[i] for i in xrange(len(docs)) if len(docs[i]) >= 20])
		print "len(extracted_times)" + str(len(extracted_times))

with open(extracted_times_file, 'wb') as f_save:
	print "open pickle file for save: " + extracted_times_file
	cPickle.dump(extracted_times, f_save, cPickle.HIGHEST_PROTOCOL)
	print "end save"