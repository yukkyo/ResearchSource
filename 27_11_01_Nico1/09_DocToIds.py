#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle

# 全文書(約50万)の各文書を語彙idの集合に変換する
# また全語彙について、1つでも出現したことのある文書の数 vocab_doc_freq[len(vocabs)] を作る

MAX_PICKLE_FILES = 6

corpus_files = "../../ResearchData/After_Extract_Over20Words/over_20words_docs"
# all_docs_files = "../../ResearchData/After_Remove/after_remove_stop_word"
vocab_to_id_file = "../../ResearchData/After_Extract_Over20Words/dic_vocab_to_id0.pkl"
# id_to_vocab_file = "../../ResearchData/After_Extract_Over20Words/list_id_to_vocab0.pkl"
corpus_by_ids_file = "../../ResearchData/After_Extract_Over20Words/corpus_by_ids0.pkl"
vocab_doc_freq_file = "../../ResearchData/After_Extract_Over20Words/vocab_doc_freq0.pkl"

with open(vocab_to_id_file, 'rb') as f:
	print "load: " + vocab_to_id_file
	vocab_to_id = cPickle.load(f)
	# vocab_doc_freq (語彙が出現したことのあるdocの数)の初期化
	vocab_doc_freq = [0] * len(vocab_to_id)
	print "len(vocab_to_id): " + str(len(vocab_to_id))
	# 初期化
	corpus_by_ids = []

	for num in range(0, MAX_PICKLE_FILES):
		with open(corpus_files + str(num) + '.pkl', 'rb') as f_corpus:
			print "load: " + corpus_files + str(num)
			corpus = cPickle.load(f_corpus)
			# corpus中の全ての文書をidsに変換する
			corpus_by_ids.extend([[vocab_to_id[term] for term in doc] for doc in corpus])
			# vocab_doc_freq を作成する
			for doc in corpus:
				vocabs_in_doc = dict()
				for term in doc:
					term_vocab_id = vocab_to_id[term]
					if not vocabs_in_doc.has_key(term_vocab_id):
						vocabs_in_doc[term_vocab_id] = None
						vocab_doc_freq[term_vocab_id] += 1
			print "close: " + corpus_files + str(num)
			print "len(corpus_by_ids): " + str(len(corpus_by_ids))

	# save corpus_by_ids
	with open(corpus_by_ids_file, 'wb') as f_save:
		print "save : " + corpus_by_ids_file
		cPickle.dump(corpus_by_ids, f_save, cPickle.HIGHEST_PROTOCOL)
		print "end"
	# save vocab_doc_freq
	with open(vocab_doc_freq_file, 'wb') as f_save:
		print "save : " + vocab_doc_freq_file
		cPickle.dump(vocab_doc_freq, f_save, cPickle.HIGHEST_PROTOCOL)
		print "end"