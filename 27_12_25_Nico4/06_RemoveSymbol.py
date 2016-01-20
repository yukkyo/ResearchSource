#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import re

# 形態素解析した結果から、記号や数字のみの単語を削除する

after_mecab_file = "../../ResearchData/Experiment4/after_mecab/after_mecab"
f_docs_without_symbols = "../../ResearchData/Experiment4/after_mecab/docs_without_symbols"

pattern = re.compile(u"[.]*[a-zA-Zぁ-んァ-ン一-龥]+[.]*")
patternForTag = re.compile(u"[ぁ-んァ-ンーa-zA-Z0-9一-龠０-９\-\r]*[ぁ-んァ-ン一-龥]+[ぁ-んァ-ンーa-zA-Z0-9一-龠０-９\-\r]*")
video_count = 0
add_file_name_list = ["1.pkl", "2.pkl"]

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
			doc_without_symbols = []
			for w in doc:
				if not w.find('___'):
					# タグであったとき
					if len(w) > 1 and (len(w) > 2 or patternForTag.match(w)):
						doc_without_symbols.append(w)
				else:
					# タグでなかったとき
					if pattern.match(w):
						doc_without_symbols.append(w)
			# doc_without_symbols = [w for w in doc if (w.find('___') == 0 and )]
			# doc_without_symbols.extend([w for w in doc if pattern.match(w)])
			append(doc_without_symbols)
			video_count += 1
			if (video_count + 1) % 10000 == 0 :
				print "end videos: " + str(video_count + 1)
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