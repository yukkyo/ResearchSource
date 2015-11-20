#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Tagの辞書からMecabに追加するためのCSVを作る

import codecs
import shelve



# MAX_DAT_FILES = 10
# MAX_DAT_FILES = 1926
MAX_DAT_FILES = 500
FILES_PER_SHELVE = 50

VideoCount = 0

# initialize tag dictionary
# csv_file_name = "sample_file.csv"
csv_file_name = "tag_csv_for_mecab.csv"
tag_dic_file_name = "../../ResearchData/All_Tags"

with codecs.open(csv_file_name, mode = 'w', encoding = 'utf-8') as f:
	dic = shelve.open(tag_dic_file_name)
	all_tags = dic["TagCountOver10"]
	dic.close()
	# all_tags = ['りんご','ニコニコ動画','あああああ','ピチュン']
	tag_convert_finished_count = 0
	for tag in all_tags:
		if( len(tag) > 4 and tag.find(",") == -1):
			score = max(-32768.0, (6000 - 200 * len(tag) / 3 * 1.3))
			tag_csv = "%s,-1,-1,%f,名詞,固有名詞,一般,*,*,*,%s,*,*,nico_tag_over10\n" % (tag,score,tag)
			f.write(tag_csv.decode('utf-8'))
			tag_convert_finished_count += 1
			print tag_convert_finished_count