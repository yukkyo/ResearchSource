#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle

# ファイルを読み取って、全文書（約50万文書）の語彙-idの辞書をつくる
# ここで出現回数が10回以下のものは除く
# またここで全文書（トレーニング、テスト）をid化したい
# テスト文書はタイトルと本文のみから作る
# テスト文書のタグのみも作る？

f_docs_without_symbols = "../../ResearchData/Experiment2/after_mecab/docs_without_symbols"
f_vocab_to_id = "../../ResearchData/Experiment2/after_convert_id/dic_vocab_id.pkl"
f_id_to_vocab = "../../ResearchData/Experiment2/after_convert_id/list_id_vocab.pkl"
f_docs_as_ids_train = "../../ResearchData/Experiment2/after_convert_id/docs_as_id_train.pkl"
f_docs_as_ids_test = "../../ResearchData/Experiment2/after_convert_id/docs_as_id_test.pkl"
f_tags_test_docs = "../../ResearchData/Experiment2/after_convert_id/tags_test_docs.pkl"

convert_end_docs = 0

# count all vocab
add_f_names = ["1.pkl", "2.pkl"]
all_word_count = 0
vocab_count = dict()
for f_name in add_f_names:
	with open(f_docs_without_symbols + f_name, 'rb') as f:
		print "open: " + f_docs_without_symbols + f_name+ '.pkl'
		docs = cPickle.load(f)
		for doc in docs:
			for w in doc:
				if w in vocab_count:
					vocab_count[w] += 1
				else:
					vocab_count[w] = 0
				all_word_count += 1
		print "end: " + f_docs_without_symbols + '.pkl'
print "all words in training: " + str(all_word_count)

# make vocab-id dic over 10 count
vocab_to_id = dict()
id_to_vocab = []
print "make vocab-id dic over 10 count"

for vocab, count in vocab_count.iteritems():
	if count > 10:
		vocab_to_id[vocab] = len(id_to_vocab)
		id_to_vocab.append(vocab)
vocab_count = None
print "len(id_to_vocab) = " + str(len(id_to_vocab))

with open(f_vocab_to_id, 'wb') as f:
	print "open for saving: " + f_vocab_to_id
	cPickle.dump(vocab_to_id, f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"

with open(f_id_to_vocab, 'wb') as f:
	print "open for saving: " + f_id_to_vocab
	cPickle.dump(id_to_vocab, f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"
id_to_vocab = None

# make docs_as_ids_train
docs_as_ids_train = []
docs_as_ids_test = []
tags_of_test_docs = []
add_f_names = ["1.pkl", "2.pkl"]
end_docs = 0
end_words = 0
for add_f_name in add_f_names:
	with open(f_docs_without_symbols + f_name, 'rb') as f:
		print "open: " + f_docs_without_symbols + '.pkl'
		docs = cPickle.load(f)
		for doc in docs:
			doc_as_ids = []
			for w in doc:
				if w in vocab_to_id:
					doc_as_ids.append(vocab_to_id[w])
					end_words += 1
			docs_as_ids_train.append(doc_as_ids)
			end_docs += 1
		print "end: " + f_docs_without_symbols + '.pkl'
print "end_docs: " + str(end_docs)
print "end_words: " + str(end_words)

with open(f_docs_as_ids_train, 'wb') as f:
	print "open: " + f_docs_as_ids_train
	cPickle.dump(docs_as_ids_train, f, cPickle.HIGHEST_PROTOCOL)
	print "end"

with open(f_docs_without_symbols + '_test.pkl', 'rb') as f:
	print "open: " + f_docs_without_symbols + '_test.pkl'
	docs = cPickle.load(f)
	for doc in docs:
		doc_as_ids = []
		tags = []
		for w in doc:
			if w.find('___') == 0:
				tags.append(w)
			else:
				if w in vocab_to_id:
					doc_as_ids.append(vocab_to_id[w])
		docs_as_ids_test.append(doc_as_ids)
		tags_of_test_docs.append(tags)
with open(f_docs_as_ids_test, 'wb') as f:
	print "open: " + f_docs_as_ids_test
	cPickle.dump(docs_as_ids_test, f, cPickle.HIGHEST_PROTOCOL)
	print "end saving"

with open(f_tags_test_docs, 'wb') as f:
	print "open: " + f_tags_test_docs
	cPickle.dump(tags_of_test_docs, f, cPickle.HIGHEST_PROTOCOL)
	print "end"