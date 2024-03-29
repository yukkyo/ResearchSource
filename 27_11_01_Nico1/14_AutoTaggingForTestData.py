#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import numpy

# テストデータcorpus[100000:110000]に対してタグを50個まで推薦する

# corpus_by_ids_file = "../../ResearchData/After_Extract_Over20Words/corpus_by_ids0.pkl"
# vocab_doc_freq_file = "../../ResearchData/After_Extract_Over20Words/vocab_doc_freq0.pkl"
id_to_vocab_file = "../../ResearchData/After_Extract_Over20Words/list_id_to_vocab0.pkl"

# corpus_by_ids_over10count_file = "../../ResearchData/After_Extract_Over20Words/corpus_by_ids_over10count.pkl"
vocabs_ids_over10count_file = "../../ResearchData/After_Extract_Over20Words/vocabs_ids_over10count.pkl"

new_corpus_by_ids_file = "../../ResearchData/After_Extract_Over20Words/new_corpus_by_ids.pkl"
convert_vocabs_ids_old_to_new_file = "../../ResearchData/After_Extract_Over20Words/convert_vocabs_ids_old_to_new.pkl"
convert_vocabs_ids_new_to_old_file = "../../ResearchData/After_Extract_Over20Words/convert_vocabs_ids_new_to_old.pkl"

experiment_result_file = "../../ResearchData/After_Extract_Over20Words/experiment_result/"

K = 100
ITERATION = 250
ALPHA = 0.1
BETA = 0.01
MAX_DOCS = 100000
MAX_TEST_DOCS = 1000
MAX_AUTO_TAGGING = 50
# corpus等の読み込み
new_corpus = None
id_to_vocab = None
vocab_topic_matrix_norm = None
vocab_topic_matrix_zero = None
convert_ids_new_to_old = None

file_name_N_norm = experiment_result_file + "K" + str(K) + 'a' + str(ALPHA) + 'b' + str(BETA) + 'i' + str(ITERATION) + '_N_norm.pkl'
file_name_N_zero = experiment_result_file + "K" + str(K) + 'a' + str(ALPHA) + 'b' + str(BETA) + 'i' + str(ITERATION) + '_N_zero.pkl'
result_tags_file = experiment_result_file + "K" + str(K) + 'a' + str(ALPHA) + 'b' + str(BETA) + 'i' + str(ITERATION) + '_result_tags.pkl'

# corpus等のロード
with open(new_corpus_by_ids_file, 'rb') as f1:
	print "loading: " + new_corpus_by_ids_file
	corpus = cPickle.load(f1)

with open(id_to_vocab_file, 'rb') as f2:
	print "loading: " + id_to_vocab_file
	id_to_vocab = cPickle.load(f2)

with open(file_name_N_norm, 'rb') as f3:
	print "loading: " + file_name_N_norm
	vocab_topic_matrix_norm = cPickle.load(f3)

with open(file_name_N_zero, 'rb') as f4:
	print "loading: " + file_name_N_zero
	vocab_topic_matrix_zero = cPickle.load(f4)

# タグ一覧(新しいidでの)を作る
tag_ids_new = set([])
with open(convert_vocabs_ids_new_to_old_file, 'rb') as f:
	print "loading: " + convert_vocabs_ids_new_to_old_file
	voca_id_new_to_old = cPickle.load(f)
	print "make tag_ids_new"
	for i in xrange(len(voca_id_new_to_old)):
		if id_to_vocab[voca_id_new_to_old[i]].find('___') == 0:
			tag_ids_new.add(i)
	print "end make tag_ids_new"

# 各文書について、タグをのぞいた中からトピックの重みを算出する
topics_weight_docs = numpy.zeros((MAX_TEST_DOCS, K))
print "make topics_weight_docs"
for i, doc in enumerate(corpus[MAX_DOCS:MAX_DOCS + MAX_TEST_DOCS]):
	for vocab in doc:
 		if not vocab in tag_ids_new:
 			topics_weight_docs[i] += vocab_topic_matrix_norm[vocab]

# かけざんする
print "vocab_topic_matrix_zero dot topics_weight_docs"
print "test vocab_topic_matrix_zero"
for i in range(10):
	if numpy.sum(vocab_topic_matrix_zero[i+500]) > 0:
		print id_to_vocab[voca_id_new_to_old[i+500]]
                print vocab_topic_matrix_zero[i+500]
for i in range(20):
        print id_to_vocab[voca_id_new_to_old[i]]
        print vocab_topic_matrix_zero[i]
only_tags_docs = vocab_topic_matrix_zero.dot(topics_weight_docs.transpose())
only_tags_docs = only_tags_docs.transpose()
print numpy.shape(only_tags_docs)

# トピックの重みから推薦する単語(新id)を決める
result_tags = numpy.zeros((MAX_TEST_DOCS, MAX_AUTO_TAGGING)).astype(numpy.int64)
print "auto tagging by topicc weight of docs"
for i in xrange(MAX_TEST_DOCS):
	result_tags[i] = numpy.argsort(only_tags_docs[i])[-MAX_AUTO_TAGGING:][::-1]
print numpy.shape(result_tags)
print "auto tagging end"

print "sample tags"
for tag in result_tags[400]:
	print id_to_vocab[voca_id_new_to_old[tag]]

with open(result_tags_file, 'wb') as f:
	print "open for saving: " + result_tags_file
 	cPickle.dump(result_tags, f, cPickle.HIGHEST_PROTOCOL)
 	print "saving is end"