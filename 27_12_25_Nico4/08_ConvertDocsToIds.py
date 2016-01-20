#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle

# ファイルを読み取って、全文書（約50万文書）の語彙-idの辞書をつくる
# ここで出現回数が10回以下のものは除く
# またここで全文書（トレーニング、テスト）をid化したい
# テスト文書はタイトルと本文のみから作る
# テスト文書のタグのみも作る？

f_docs_without_symbols = "../../ResearchData/Experiment4/after_mecab/docs_without_symbols"
f_vocab_to_id = "../../ResearchData/Experiment4/after_convert_id/dic_vocab_id.pkl"
f_id_to_vocab = "../../ResearchData/Experiment4/after_convert_id/list_id_vocab.pkl"
f_docs_as_ids_train = "../../ResearchData/Experiment4/after_convert_id/docs_as_id_train.pkl"
f_docs_as_ids_test = "../../ResearchData/Experiment4/after_convert_id/docs_as_id_test.pkl"
f_tags_test_docs = "../../ResearchData/Experiment4/after_convert_id/tags_test_docs.pkl"

Convert_end_docs = 0
# count all vocab
add_f_names = ["1.pkl", "2.pkl"]
all_word_count = 0
vocab_count = dict()

"""Count vocab count"""
for f_name in add_f_names:
	with open(f_docs_without_symbols + f_name, 'rb') as f:
		print "open: " + f_docs_without_symbols + f_name
		docs = cPickle.load(f)
		for doc in docs:
			for w in doc:
				if w in vocab_count:
					vocab_count[w] += 1
				else:
					vocab_count[w] = 0
				all_word_count += 1
		print "end: " + f_docs_without_symbols + f_name
print "all words in training: " + str(all_word_count)

tag_set = set([])
for vocab in vocab_count.keys():
	if vocab.find('___') == 0 and vocab_count[vocab] > 10:
		tag_set.add(vocab)
print "len(tag_set): " + str(len(tag_set))

# sort by value(count)
# vocab_count = sorted(vocab_count.items(), key=lambda x:x[1], reverse=True)
count_over10 = 0
print "len(vocab_count): " + str(len(vocab_count))
for v in vocab_count.values():
	if v > 10:
		count_over10 += 1
print "count_over10: " + str(count_over10)
count_over10 *= 0.05
# count_over10 *= 0.80
count = 0
vocab_to_id = dict()
id_to_vocab = []
for k, v in sorted(vocab_count.items(), key=lambda x:x[1], reverse=True):
	if k.find('___') == 0:
		if v > 10:
			vocab_to_id[k] = len(id_to_vocab)
			id_to_vocab.append(k)
	else:
		# タグじゃない場合
		# if ('___' + k) in tag_set:
		# 	if v > 10:
		# 		vocab_to_id[k] = len(id_to_vocab)
		# 		id_to_vocab.append(k)
		# 	else:
		# 		count += 1
		# el
		if count > count_over10:
			if v > 10:
				vocab_to_id[k] = len(id_to_vocab)
				id_to_vocab.append(k)
		else:
			count += 1

print "len(vocabs): " + str(len(id_to_vocab))
print "len(tags): " + str(len([v for v in id_to_vocab if v.find('___') == 0]))

with open(f_vocab_to_id, 'wb') as f:
	print "open for saving: " + f_vocab_to_id
	cPickle.dump(vocab_to_id, f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"

with open(f_id_to_vocab, 'wb') as f:
	print "open for saving: " + f_id_to_vocab
	cPickle.dump(id_to_vocab, f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"

# make docs_as_ids_train
docs_as_ids_train = []
docs_as_ids_test = []
tags_of_test_docs = []
add_f_names = ["1.pkl", "2.pkl"]
end_docs = 0
end_words = 0

"""Make training data"""
for f_name in add_f_names:
	with open(f_docs_without_symbols + f_name, 'rb') as f:
		print "open: " + f_docs_without_symbols + f_name
		docs = cPickle.load(f)
		for doc in docs:
			doc_as_ids = []
			tag_count = 0
			nontag_count = 0
			for w in doc:
				if w in vocab_to_id:
					doc_as_ids.append(vocab_to_id[w])
					end_words += 1
					if w in tag_set:
						tag_count += 1
					else:
						nontag_count += 1
			if nontag_count > 4 and tag_count > 0:
				docs_as_ids_train.append(doc_as_ids)
			end_docs += 1
		print "end: " + f_docs_without_symbols + f_name
print "end_docs: " + str(end_docs)
print "end_words: " + str(end_words)
print "len(docs_as_ids): " + str(len(docs_as_ids_train))

with open(f_docs_as_ids_train, 'wb') as f:
	print "open: " + f_docs_as_ids_train
	cPickle.dump(docs_as_ids_train, f, cPickle.HIGHEST_PROTOCOL)
	print "end"

print "sample docs"
for i in range(10):
	print "docs[" + str(500000 + i) + "]"
	print "----------------------"
	for v in docs_as_ids_train[500000 + i]:
		print str(v) + ": "+ id_to_vocab[v] + " count: " + str(vocab_count[id_to_vocab[v]])
	print "----------------------"
