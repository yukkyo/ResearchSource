#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle

# 20語未満の文書を取り除く

MAX_PICKLE_FILES = 6

after_remove_file = "../../ResearchData/After_Remove/after_remove_stop_word"
extracted_file = "../../ResearchData/After_Extract_Over20Words/over_20words_docs"
total_docs_count = 0

# for num in range(0, MAX_PICKLE_FILES):
# 	with open(after_remove_file + str(num) + '.pkl', 'rb') as f:
# 		after_remove_docs = cPickle.load(f)
# 		print "len(after_remove_docs) :" + str(len(after_remove_docs))
# 		# 各文書から20語未満のものを取り除く
# 		extracted_docs = [doc for doc in after_remove_docs if len(doc) >= 20]
# 		after_remove_docs = None
# 		print "len(extracted_docs)" + str(len(extracted_docs))
# 		with open(extracted_file + str(num) + '.pkl', 'wb') as f_save:
# 			print "open pickle file for save: over_20words_file" + str(num)
# 			cPickle.dump(extracted_docs, f_save, cPickle.HIGHEST_PROTOCOL)
# 			total_docs_count += len(extracted_docs)
# 			extracted_docs = None
# 			print "end save"

# for num in range(0, MAX_PICKLE_FILES):
# 	with open(extracted_file + str(num) + '.pkl', 'rb') as f:
# 		extracted_docs = cPickle.load(f)
# 		total_docs_count += len(extracted_docs)

# print "total_docs_count: " + str(total_docs_count)