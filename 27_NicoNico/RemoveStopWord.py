#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import re

# 形態素解析した結果から、いらない単語を除去する

MAX_PICKLE_FILES = 6
# MAX_SHELVE_FILES = 6
FILES_PER_SHELVE = 50

video_count = 0
dic_file_name = "../../ResearchData/All_Tags"
after_mecab_file = "../../ResearchData/After_Mecab/after_mecab"
after_remove_file = "../../ResearchData/After_Remove/after_remove_stop_word"
# pattern = re.compile(u"[ぁ-んァ-ン一-龥]+")
pattern = re.compile(u"[0-9]*[a-zA-Zぁ-んァ-ン一-龥]+[0-9]*")

for num in range(0, MAX_PICKLE_FILES):
	# pickle file open
	with open(after_mecab_file + str(num) + '.pkl', 'rb') as f:
		print "open pickle file for load: after_mecab_file" + str(num)
		after_mecabs = cPickle.load(f)
		print "convert str to unicode (decode)"
		after_mecabs_decoded = [[word.decode('utf-8') for word in after_mecab] for after_mecab in after_mecabs]
		print "len(after_mecabs_decoded):" + str(len(after_mecabs_decoded))
		after_mecabs = None
		documents_after_remove = []
		append = documents_after_remove.append
		# 各文書からいらない単語を除去する
		for document in after_mecabs_decoded:
			doc_after_remove = [w for w in document if not w.find('___')]
			doc_after_remove.extend([w for w in document if pattern.match(w)])
			append(doc_after_remove)
			video_count += 1
			if video_count % 2000 == 0 :
				print "end videos: " + str(video_count)
		print "len(documents_after_remove):" + str(len(documents_after_remove))
		after_mecabs_decoded = None
		print 'convert unicode to str (encode)'
		encoded_documents = [[word.encode('utf-8') for word in document] for document in documents_after_remove]
		documents_after_remove = None
		print "len(encoded_documents):" + str(len(encoded_documents))
		with open(after_remove_file + str(num) + '.pkl', 'wb') as f_save:
			print "open pickle file for save: after_remove_file" + str(num)
			cPickle.dump(encoded_documents, f_save, cPickle.HIGHEST_PROTOCOL)
			print "end save"
			print "end videos: " + str(video_count)