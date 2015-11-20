#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle

# 全文書(約50万)に対してLDA(Collapsed Gibbs Sampling)を適用する
# 処理前は約110万あった語彙から、頻度が高すぎる、もしくは低すぎるものを削除する

corpus_by_ids_file = "../../ResearchData/After_Extract_Over20Words/corpus_by_ids0.pkl"
vocab_doc_freq_file = "../../ResearchData/After_Extract_Over20Words/vocab_doc_freq0.pkl"
id_to_vocab_file = "../../ResearchData/After_Extract_Over20Words/list_id_to_vocab0.pkl"


corpus_by_ids_over10count_file = "../../ResearchData/After_Extract_Over20Words/corpus_by_ids_over10count.pkl"
vocabs_ids_over10count_file = "../../ResearchData/After_Extract_Over20Words/vocabs_ids_over10count.pkl"

new_corpus_by_ids_file = "../../ResearchData/After_Extract_Over20Words/new_corpus_by_ids.pkl"
convert_vocabs_ids_old_to_new_file = "../../ResearchData/After_Extract_Over20Words/convert_vocabs_ids_old_to_new.pkl"
convert_vocabs_ids_new_to_old_file = "../../ResearchData/After_Extract_Over20Words/convert_vocabs_ids_new_to_old.pkl"


# まず全語彙について、出現した回数をカウントする
all_vocabs_count = []
with open(id_to_vocab_file, 'rb') as f:
	print "load: " + id_to_vocab_file
	id_to_vocab = cPickle.load(f)
	all_vocabs_count = [0] * len(id_to_vocab)
	print "len(id_to_vocab): " + str(len(id_to_vocab))

with open(corpus_by_ids_file, 'rb') as f:
	print "load: " + corpus_by_ids_file
	corpus_by_ids = cPickle.load(f)
	print "len(corpus_by_ids)" + str(len(corpus_by_ids))
	# 文書がちゃんと格納されているか確認
	# with open(id_to_vocab_file, 'rb') as f_load:
	# 	print "load: " + id_to_vocab_file
	# 	id_to_vocab = cPickle.load(f_load)
		# for i in range(20, 25):
		# 	for w in corpus_by_ids[i]:
		# 		print id_to_vocab[w]
	# id_to_vocab = None
	for doc in corpus_by_ids:
		for w in doc:
			all_vocabs_count[w] += 1

# 辞書がたに変換
# all_vocabs_count_dic = dict(zip(range(0, len(all_vocabs_count)), all_vocabs_count))

# under10count_words_ids = [i for i in range(len(all_vocabs_count)) if all_vocabs_count[i] <= 10]
# print "count of words lower than 10 count: " + str(len(under10count_words_ids))
# for i in range(10):
# 	print under10count_words_ids[i]
# 	print id_to_vocab[under10count_words_ids[i]]

vocabs_ids_over10count = set([i for i in range(len(all_vocabs_count)) if all_vocabs_count[i] > 10])
convert_vocabs_ids_old_to_new = dict(zip(vocabs_ids_over10count, range(0, len(vocabs_ids_over10count))))
convert_vocabs_ids_new_to_old = dict(zip(range(0, len(vocabs_ids_over10count)), vocabs_ids_over10count))
print "count of words over than 10 count: " + str(len(vocabs_ids_over10count))
print "all vocabs count: " + str(len(all_vocabs_count))

print "make corpus_by_ids_over10count"
corpus_by_ids_over10count = [[w for w in doc if w in vocabs_ids_over10count] for doc in corpus_by_ids]
print "end make corpus"
print "total docs in corpus_by_ids: " + str(len(corpus_by_ids))
print "total docs in corpus_by_ids_over10count: " + str(len(corpus_by_ids_over10count))
print "total words in corpus_by_ids: " + str(sum([len(doc) for doc in corpus_by_ids]))
print "total words in corpus_by_ids_over10count: " + str(sum([len(doc) for doc in corpus_by_ids_over10count]))

# with open(corpus_by_ids_over10count_file, 'wb') as f:
# 	print "open for save: " + corpus_by_ids_over10count_file
# 	cPickle.dump(corpus_by_ids_over10count, f, cPickle.HIGHEST_PROTOCOL)
# 	print "save end"

# with open(vocabs_ids_over10count_file, 'wb') as f:
# 	print "open for save: " + corpus_by_ids_over10count_file
# 	cPickle.dump(vocabs_ids_over10count, f, cPickle.HIGHEST_PROTOCOL)
# 	print "save end"

# このままだと前の語彙
print "make new corpus_br_ids"
new_corpus_by_ids = [[convert_vocabs_ids_old_to_new[w] for w in doc] for doc in corpus_by_ids_over10count]
print "total docs in new_corpus: " + str(len(new_corpus_by_ids))
print "total words in new_corpus" + str(sum([len(doc) for doc in new_corpus_by_ids]))

with open(new_corpus_by_ids_file, 'wb') as f:
	print "open for save: " + new_corpus_by_ids_file
	cPickle.dump(new_corpus_by_ids, f, cPickle.HIGHEST_PROTOCOL)
	print "save end"

with open(convert_vocabs_ids_old_to_new_file, 'wb') as f:
	print "open for save: " + convert_vocabs_ids_old_to_new_file
	cPickle.dump(convert_vocabs_ids_old_to_new, f, cPickle.HIGHEST_PROTOCOL)
	print "save end"

with open(convert_vocabs_ids_new_to_old_file, 'wb') as f:
	print "open for save: " + convert_vocabs_ids_new_to_old_file
	cPickle.dump(convert_vocabs_ids_new_to_old, f, cPickle.HIGHEST_PROTOCOL)
	print "save end"