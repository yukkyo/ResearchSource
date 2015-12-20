#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import numpy

# もとめた全文書に割り振ったトピックから、各語彙が各トピックに割り振られた回数を示す
# V x K 行列を作る。また正規化したものとタグ以外を0にしたものも作る

f_estimated_result = "../../ResearchData/Experiment2/after_estimated/"
f_corpus_by_ids_train = "../../ResearchData/Experiment2/after_convert_id/docs_as_id_train.pkl"
f_id_to_vocab = "../../ResearchData/Experiment2/after_convert_id/list_id_vocab.pkl"
f_vocab_to_id = "../../ResearchData/Experiment2/after_convert_id/dic_vocab_id.pkl"
fpath_exp_result = "../../ResearchData/Experiment2/after_LDA/"

K = 400
V = None
ITERATION = 150
ALPHA = 0.1
BETA = 0.01

# id_to_vocabと語彙の大きさVの取得
id_to_vocab = None
with open(f_id_to_vocab, 'rb') as f:
	print "loading: " + f_id_to_vocab
	id_to_vocab = cPickle.load(f)
	V = len(id_to_vocab)
	print "len(id_to_vocab) = V " + str(V)

# VK行列の読み込み
f_VKmatrix = fpath_exp_result + "k" + str(K) + 'a' + str(ALPHA) + 'b' + str(BETA) + 'i' + str(ITERATION) + '_VKmatrix'
f_VKmatrix_norm = f_VKmatrix + '_norm.pkl'
f_VKmatrix_nontagzero = f_VKmatrix + '_nontagzero.pkl'
VK_matrix = None
with open(f_VKmatrix + '.pkl', 'rb') as f:
	print "loading: " + f_VKmatrix
	VK_matrix = cPickle.load(f)
	print "loading end"

# VK行列nを初期化する
VK_matrix_normalized = numpy.zeros((V, K))
VK_matrix_nontag_zero = numpy.zeros((V, K))

# 各語彙について、正規化したn'	を作る
print "normalize vocab_topic_matrix"
for i in xrange(V):
	if numpy.sum(VK_matrix[i]) != 0:
		VK_matrix_normalized[i] = VK_matrix[i] / VK_matrix[i].sum()
		VK_matrix_nontag_zero[i] = VK_matrix_normalized[i]

# nのうち、タグ以外の単語に関する行の数値を0にしたn_zeroを作る
print "zero nontag vocab"
count = 0
for i in xrange(V):
	if id_to_vocab[i].find('___') != 0:
		count += 1
		VK_matrix_nontag_zero[i] = 0.
print "all vocabs: " + str(V)
print "nontag vocabs: " + str(count)
print "tag vocabs: " + str(V - count)

# VK_matrix_normとVK_matrix_nontag_zeroの保存
with open(f_VKmatrix_norm, 'wb') as f:
	print "saving: " + f_VKmatrix_norm
	cPickle.dump(VK_matrix_normalized, f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"
with open(f_VKmatrix_nontagzero, 'wb') as f:
	print "saving: " + f_VKmatrix_nontagzero
	cPickle.dump(VK_matrix_nontag_zero, f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"