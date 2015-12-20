#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import numpy
from sklearn import svm

# もとめた全文書に割り振ったトピックから、各語彙が各トピックに割り振られた回数を示す
# V x K 行列を作る。また正規化したものとタグ以外を0にしたものも作る

f_estimated_result = "../../ResearchData/Experiment2/after_estimated/"
f_corpus_by_ids_train = "../../ResearchData/Experiment2/after_convert_id/docs_as_id_train.pkl"
f_id_to_vocab = "../../ResearchData/Experiment2/after_convert_id/list_id_vocab.pkl"
f_vocab_to_id = "../../ResearchData/Experiment2/after_convert_id/dic_vocab_id.pkl"
fpath_exp_result = "../../ResearchData/Experiment2/after_LDA/"
fpath_svm_result = "../../ResearchData/Experiment2/after_SVM/"

K = 400
V = None
ITERATION = 150
ALPHA = 0.1
BETA = 0.01
MAX_TRAIN_DOCS = 500000
MAX_TEST_DOCS = 10000
MAX_AUTO_TAGGING = 50
corpus = None
train_corpus = None
test_corpus = None
id_to_vocab = None
train_tags_count = []

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
VK_matrix = None
with open(f_VKmatrix_norm, 'rb') as f:
	print "loading: " + f_VKmatrix
	VK_matrix = cPickle.load(f)
	print "loading end"

# コーパスの読み込み
with open(f_corpus_by_ids_train, 'rb') as f:
	print "loading: " + f_corpus_by_ids_train
	corpus = cPickle.load(f)
	train_corpus = corpus[:MAX_TRAIN_DOCS]
	test_corpus = corpus[MAX_TRAIN_DOCS : MAX_TRAIN_DOCS + MAX_TEST_DOCS]
	corpus = None
	print "len(train_corpus): " + str(len(train_corpus))
	print "len(test_corpus): " + str(len(test_corpus))

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

# コーパス中のタグ数をカウントする
train_tags_count = [len([v for v in doc if v in tag_ids_set]) for doc in train_corpus]

# コーパス中のトレーニング文書をトピックの重みで表す
print "calc topic weights of training corpus"
topic_weight_train = []
for doc in train_corpus:
	topic_weight = numpy.zeros(K)
	for w in doc:
		topic_weight += VK_matrix[w]
	topic_weight_train.append(topic_weight)

# コーパス中のテスト文書をトピックの重みで表す
print "calc topic weights of training corpus"
topic_weight_test = []
for doc in test_corpus:
	topic_weight = numpy.zeros(K)
	for w in doc:
		if w not in tag_ids_set:
			topic_weight += VK_matrix[w]
	topic_weight_test.append(topic_weight)

# テスト文書のタグ数を推定する
print "estimate"
clf = svm.LinearSVC()
print "end make svm"
clf.fit(topic_weight_train, train_tags_count)
estimated_tags_count = clf.predict(topic_weight_test)
print "estimate is end"

# 推定したタグ数を保存する
with open(fpath_svm_result + 'estimated_tags_count.pkl','wb') as f:
	print "saving: " + fpath_svm_result + 'estimated_tags_count.pkl'
	cPickle.dump(estimated_tags_count, f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"

# トレーニング文書中のトピックの重みを正規化する
topic_weight_train_norm = []
for weight in topic_weight_train:
	if weight.sum() == 0.:
		topic_weight_train_norm.append(weight)
	else:
		topic_weight_train_norm.append(weight / weight.sum())

# テスト文書のトピックの重みを正規化する
topic_weight_test_norm = []
for weight in topic_weight_test:
	if weight.sum() == 0.:
		topic_weight_test_norm.append(weight)
	else:
		topic_weight_test_norm.append(weight / weight.sum())

# テスト文書のタグ数を推定する
print "estimate"
clf2 = svm.LinearSVC()
print "end make svm"
clf2.fit(topic_weight_train_norm, train_tags_count)
estimated_tags_count_norm = clf2.predict(topic_weight_test_norm)
print "estimate is end"

# 推定したタグ数を保存する
with open(fpath_svm_result + 'estimated_tags_count_norm.pkl','wb') as f:
	print "saving: " + fpath_svm_result + 'estimated_tags_count_norm.pkl'
	cPickle.dump(estimated_tags_count_norm, f, cPickle.HIGHEST_PROTOCOL)
	print "saving is end"