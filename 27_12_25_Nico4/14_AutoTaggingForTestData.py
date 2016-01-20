#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import numpy

# テストデータcorpus[500000:510000]に対してタグを50個まで推薦する
f_path_estimated_result = "../../ResearchData/Experiment4/after_estimated/"
f_corpus_by_ids_test = "../../ResearchData/Experiment4/after_convert_id/docs_as_id_train.pkl"
f_id_to_vocab = "../../ResearchData/Experiment4/after_convert_id/list_id_vocab.pkl"
f_vocab_to_id = "../../ResearchData/Experiment4/after_convert_id/dic_vocab_id.pkl"
fpath_matrix = "../../ResearchData/Experiment4/after_Matrix/"

K = 400
V = None
ITERATION = 250
ALPHA = 0.5
BETA = 0.5
MAX_TRAIN_DOCS = 500000
MAX_TEST_DOCS = 10000
MAX_AUTO_TAGGING = 50
new_corpus = None
id_to_vocab = None
vocab_to_id = None
VK_matrix_norm = None
VK_matrix_zero = None

f_estimated_result = f_path_estimated_result + "k" + str(K) + 'a' + str(ALPHA) + 'b' + str(BETA) + 'i' + str(ITERATION) + '.pkl'

# VK行列の読み込み
f_VKmatrix = fpath_matrix + "k" + str(K) + 'a' + str(ALPHA) + 'b' + str(BETA) + 'i' + str(ITERATION) + '_VKmatrix'
f_VKmatrix_norm = f_VKmatrix + '_norm.pkl'
f_VKmatrix_zero = f_VKmatrix + '_nontagzero.pkl'
# 語彙トピック行列（正規化済）のロード
with open(f_VKmatrix_norm, 'rb') as f:
	print "loading: " + f_VKmatrix_norm
	VK_matrix_norm = cPickle.load(f)
# 語彙トピック行列（タグ以外の語彙を0にしたもの）のロード
with open(f_VKmatrix_zero, 'rb') as f:
	print "loading: " + f_VKmatrix_zero
	VK_matrix_zero = cPickle.load(f)
# test用文書のロード
with open(f_corpus_by_ids_test, 'rb') as f:
	print "loading: " + f_corpus_by_ids_test
	corpus = cPickle.load(f)
	testDocs = corpus[MAX_TRAIN_DOCS : MAX_TRAIN_DOCS + MAX_TEST_DOCS]
	corpus = None
	print "len(testdocs) = len(corpus[randnums]) = " + str(len(testDocs))

# id_to_vocabのロード
with open(f_id_to_vocab, 'rb') as f:
	print "loading: " + f_id_to_vocab
	id_to_vocab = cPickle.load(f)

# タグ一覧(語彙id表記)を作る
tag_ids_set = set([])
count = 0
with open(f_id_to_vocab, 'rb') as f:
	print "loading: " + f_id_to_vocab
	id_to_vocab = cPickle.load(f)
	print "make tag_ids_set"
	for i in xrange(len(id_to_vocab)):
		if id_to_vocab[i].find('___') == 0:
			count += 1
			tag_ids_set.add(i)
	print "tag count: " + str(count)
	print "end make tag_ids_set"

# テストデータの各文書について、タグをのぞいた中からトピックの重みを算出する
topics_weight_docs = numpy.zeros((MAX_TEST_DOCS, K))
print "make topics_weight_docs"
count_emptydocs = 0
for i, doc in enumerate(testDocs):
	if len(doc) == 0:
		count_emptydocs += 1
		topics_weight_docs[i] += 1.
		print "doc is empty: " + str(i)
	else:
		for vocab in doc:
			if not vocab in tag_ids_set:
				topics_weight_docs[i] += VK_matrix_norm[vocab]
print "empty docs: " + str(count_emptydocs)

print "shape of topics_weight_docs: "
print numpy.shape(topics_weight_docs)

# トピックの重みから推薦する単語(新id)を決める
result_tags = numpy.zeros((MAX_TEST_DOCS, MAX_AUTO_TAGGING)).astype(numpy.int64)
print "auto tagging by topicc weight of docs"
for i in xrange(MAX_TEST_DOCS):
	only_tags_doc = VK_matrix_zero.dot(topics_weight_docs[i].transpose())
	result_tags[i] = numpy.argsort(only_tags_doc)[-MAX_AUTO_TAGGING:][-1::-1]
	if i % 2000 == 0:
		print "end docs: " + str(i)
print numpy.shape(result_tags)
print "auto tagging end"

# print "auto tagging by topicc weight of docs"
# only_tags_docs = VK_matrix_zero.dot(topics_weight_docs.transpose())
# for i in xrange(MAX_TEST_DOCS):
# 	only_tags_doc = VK_matrix_zero.dot(topics_weight_docs[i].transpose())
# 	result_tags[i] = numpy.argsort(only_tags_doc)[-MAX_AUTO_TAGGING:][::-1]
# 	if i % 2000 == 0:
# 		print "end docs: " + str(i)
# print numpy.shape(result_tags)
# print "auto tagging end"

print "sample estimated tags"
for tag in result_tags[5000]:
	print id_to_vocab[tag]

with open(f_estimated_result, 'wb') as f:
	print "open for saving: " + f_estimated_result
	cPickle.dump(result_tags, f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"
