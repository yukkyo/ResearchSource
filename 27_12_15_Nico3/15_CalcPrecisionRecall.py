#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import numpy
import csv

# 推薦した結果のPrecision Recall などを計算する
f_path_estimated_result = "../../ResearchData/Experiment2/after_estimated/"
f_corpus_by_ids_train = "../../ResearchData/Experiment2/after_convert_id/docs_as_id_train.pkl"
f_id_to_vocab = "../../ResearchData/Experiment2/after_convert_id/list_id_vocab.pkl"
f_vocab_to_id = "../../ResearchData/Experiment2/after_convert_id/dic_vocab_id.pkl"
fpath_exp_result = "../../ResearchData/Experiment2/after_LDA/"
f_rand_num_list = '../../ResearchData/Experiment2/after_LDA/random_num_list.pkl'

K = 400
V = None
ITERATION = 150
ALPHA = 0.1
BETA = 0.01
MAX_TRAIN_DOCS = 500000
MAX_TEST_DOCS = 10000
MAX_AUTO_TAGGING = 50
corpus = None
id_to_vocab = None
vocab_to_id = None
VK_matrix_norm = None
VK_matrix_zero = None
estimated_tags = None

f_estimated_result = f_path_estimated_result + "k" + str(K) + 'a' + str(ALPHA) + 'b' + str(BETA) + 'i' + str(ITERATION) + '.pkl'

# id_to_vocabの読み込み
with open(f_id_to_vocab, 'rb') as f:
	print "loading: " + f_id_to_vocab
	id_to_vocab = cPickle.load(f)

# 推定タグをロードする
with open(f_estimated_result, 'rb') as f:
	print "loading: " + f_estimated_result
	estimated_tags = cPickle.load(f)
	print "loading is end"

# 正解データを作る
print "make correct answers"
test_corpus = None
with open(f_corpus_by_ids_train) as f:
	print "loading: " + f_corpus_by_ids_train
	corpus_raw = cPickle.load(f)
	test_corpus = corpus_raw[MAX_TRAIN_DOCS : MAX_TRAIN_DOCS + MAX_TEST_DOCS]
	# test_corpus = []
	# with open(f_rand_num_list, 'rb') as f_r:
	# 	random_num_list = cPickle.load(f_r)
	# 	for i in xrange(MAX_TEST_DOCS):
	# 		test_corpus.append(corpus_raw[random_num_list[i]])
	# corpus_raw = None
	print "len(test_corpus_rand: " + str(len(test_corpus))
correct_answers = [set([v_id for v_id in d if id_to_vocab[v_id].find('___') == 0]) for d in test_corpus]

# 推薦するタグの個数毎の、precision、recall、f-measureを出す
precisions = []
recalls = []
f_measures = []
print "calc precision, recall, f-measure"
for i in range(MAX_AUTO_TAGGING):
	precision = 0.
	recall = 0.
	f_measure = 0.
	for j, est_tags in enumerate(estimated_tags):
		# 推薦するタグの個数だけ取り出す
		part_of_est_tags = set(est_tags[:i+1])
		pre = float((len(correct_answers[j] & part_of_est_tags))) / float(len(part_of_est_tags))
		if len(correct_answers[j]) == 0:
			rec = 0.
		else:
			rec = float((len(correct_answers[j] & part_of_est_tags))) / float(len(correct_answers[j]))
		precision += pre
		recall += rec
		if (pre + rec) == 0:
			f_measure += 0.
		else:
			f_measure += (2. * pre * rec) / (pre + rec)
	mean_pre = precision / float(len(estimated_tags))
	mean_rec = recall / float(len(estimated_tags))
	mean_f_measure = f_measure / float(len(estimated_tags))
	precisions.append(mean_pre)
	recalls.append(mean_rec)
	f_measures.append(mean_f_measure)

print "precision sample"
for i in range(20):
	print precisions[i]

print "recalls sample"
for i in range(20):
	print recalls[i]

print "f_measures sample"
for i in range(20):
	print f_measures[i]

with open(f_path_estimated_result + 'precisions_rand.csv', 'ab') as f:
	print "saving precisions"
	csvWriter = csv.writer(f)
	csvWriter.writerow(range(1,51))
	csvWriter.writerow(precisions)

with open(f_path_estimated_result + 'recalls_rand.csv', 'ab') as f:
	print "saving recalls"
	csvWriter = csv.writer(f)
	csvWriter.writerow(range(1,51))
	csvWriter.writerow(recalls)

with open(f_path_estimated_result + 'f_measures_rand.csv', 'ab') as f:
	print "saving f_measures"
	csvWriter = csv.writer(f)
	csvWriter.writerow(range(1,51))
	csvWriter.writerow(f_measures)