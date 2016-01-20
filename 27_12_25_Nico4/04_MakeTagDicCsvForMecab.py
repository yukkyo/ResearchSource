#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Tagの辞書からMecabに追加するためのCSVを作る
# 追加するタグは全文書において10回以上出現したタグを用いる

import codecs
import cPickle
import re

csv_file_name = "../../ResearchData/Experiment4/over10tags_for_mecab.csv"
f_tag_count_dic = "../../ResearchData/Experiment4/tag_count_dic.pkl"
pattern = re.compile(u"[.]*[ぁ-んァ-ン一-龥]+[.]*")

with codecs.open(csv_file_name, mode = 'w', encoding = 'utf-8') as f:
	tag_count_dic = None
	with open(f_tag_count_dic, "rb") as f_load:
		print "open f_tag: " + f_tag_count_dic
		tag_count_dic = cPickle.load(f_load)

	converted_tags = 0
	for tag, count in tag_count_dic.items():
		decode_tag = tag.decode('utf-8')
		if( count > 10 and len(decode_tag) > 1 and 
					(len(decode_tag) > 5 or pattern.match(decode_tag)) and tag.find(",") == -1):
			score = max(-32768.0, (6000 - 200 * len(tag) / 3 * 1.3))
			tag_csv = "%s,-1,-1,%f,名詞,固有名詞,一般,*,*,*,%s,*,*,nico_tag_over10\n" % (tag,score,tag)
			f.write(tag_csv.decode('utf-8'))
			converted_tags += 1
	print "end. all converted tags: " + str(converted_tags)