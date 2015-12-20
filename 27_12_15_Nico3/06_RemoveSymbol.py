#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import re

# 形態素解析した結果から、記号や数字のみの単語を削除する

after_mecab_file = "../../ResearchData/Experiment2/after_mecab/after_mecab"
f_docs_without_symbols = "../../ResearchData/Experiment2/after_mecab/docs_without_symbols"

pattern = re.compile(u"[0-9]*[a-zA-Zぁ-んァ-ン一-龥]+[0-9]*")
video_count = 0
add_file_name_list = ["1.pkl", "2.pkl", "_test.pkl"]

for name in add_file_name_list:
	with open(after_mecab_file + name, 'rb') as f:
		print "open: " + after_mecab_file + name
		docs = cPickle.load(f)

		print "convert str to unicode (decode)"
		docs_decoded = [ [ w.decode('utf-8') for w in doc] for doc in docs]
		print "len(docs_decoded):" + str(len(docs_decoded))
		docs = None

		docs_without_symbols = []
		append = docs_without_symbols.append

		for doc in docs_decoded:
			doc_without_symbols = [w for w in doc if not w.find('___')]
			doc_without_symbols.extend([w for w in doc if pattern.match(w)])
			append(doc_without_symbols)
			video_count += 1
			if video_count % 5000 == 0 :
				print "end videos: " + str(video_count)
		docs_decoded = None

		print 'convert unicode to str (encode)'
		docs_encoded = [[w.encode('utf-8') for w in doc] for doc in docs_without_symbols]
		docs_without_symbols = None
		print "len(docs_encoded):" + str(len(docs_encoded))

		with open(f_docs_without_symbols + name, 'wb') as f_save:
			print "open for saving: " + f_docs_without_symbols + name
			cPickle.dump(docs_encoded, f_save, cPickle.HIGHEST_PROTOCOL)
			print "end save"
			print "end videos: " + str(video_count)