#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle

# ファイルを読み取って、全文書（約50万文書）の語彙-idの辞書をつくる
MAX_PICKLE_FILES = 6

# all_doc_files = "../../ResearchData/After_Extract_Over20Words/over_20words_docs"
all_doc_files = "../../ResearchData/After_Remove/after_remove_stop_word"
vocab_to_id_file = "../../ResearchData/After_Extract_Over20Words/dic_vocab_to_id0.pkl"
id_to_vocab_file = "../../ResearchData/After_Extract_Over20Words/list_id_to_vocab0.pkl"
total_docs_count = 0

vocab_to_id = dict()
id_to_vocab = []
all_word_count = 0

def word_to_id(word):
	if word not in vocab_to_id:
		vocab_id = len(id_to_vocab)
		vocab_to_id[word] = vocab_id
		id_to_vocab.append(word)

for num in range(0, MAX_PICKLE_FILES):
	with open(all_doc_files + str(num) + '.pkl', 'rb') as f:
		print "open: " + all_doc_files + str(num)
		extracted_docs = cPickle.load(f)
		for doc in extracted_docs:
			for word in doc:
				word_to_id(word)
				all_word_count += 1
		print "close file"
		print "checked word count: " + str(all_word_count)

with open(vocab_to_id_file, 'wb') as f_save:
	print "save dic_vocab_to_id0.pkl"
	cPickle.dump(vocab_to_id, f_save, cPickle.HIGHEST_PROTOCOL)
	print "save end"

with open(id_to_vocab_file, 'wb') as f_save:
	print "save list_id_to_vocab0.pkl"
	cPickle.dump(id_to_vocab, f_save, cPickle.HIGHEST_PROTOCOL)
	print "save end"