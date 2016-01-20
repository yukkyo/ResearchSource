#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import numpy
import csv

# 推薦した結果のPrecision Recall などを計算する
f_path_estimated_result = "../../ResearchData/Experiment4/after_estimated/"
f_corpus_by_ids_train = "../../ResearchData/Experiment4/after_convert_id/docs_as_id_train.pkl"
f_id_to_vocab = "../../ResearchData/Experiment4/after_convert_id/list_id_vocab.pkl"
f_vocab_to_id = "../../ResearchData/Experiment4/after_convert_id/dic_vocab_id.pkl"
fpath_exp_result = "../../ResearchData/Experiment4/after_SVM/"
f_estimated_tagscount = '../../ResearchData/Experiment4/after_SVM/estimated_tags_count.pkl'
f_estimated_tagscount_norm = '../../ResearchData/Experiment4/after_SVM/estimated_tags_count_norm.pkl'

K = 400
V = None
ITERATION = 250
ALPHA = 0.5
BETA = 0.5
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

estimated_tagscount = None
with open(f_estimated_tagscount, 'rb') as f:
	print "open tagscount"
	estimated_tagscount = cPickle.load(f)
min_tagscount = min(estimated_tagscount)
max_tagscount = max(estimated_tagscount)
f_measure_eachcount = dict()
recall_eachcount = dict()
precision_eachcount = dict()
count_docs_eachcount = dict()
for i in range(min_tagscount, max_tagscount + 1):
	f_measure_eachcount[i] = 0.
	precision_eachcount[i] = 0.
	recall_eachcount[i] = 0.
	count_docs_eachcount[i] = len([l for l in estimated_tagscount if l == i])
for i in range(min_tagscount, max_tagscount + 1):
	print "tagscount: " + str(i) + " : " + str(count_docs_eachcount[i])

print "mintagscount: " + str(min_tagscount)
print "maxtagscount: " + str(max_tagscount)
# 推薦するタグの個数毎の、precision、recall、f-measureを出す
print "calc precision, recall, f-measure"

precision = 0.
recall = 0.
f_measure = 0.
for j, est_tags in enumerate(estimated_tags):
	# 推薦するタグの個数だけ取り出す
	part_of_est_tags = set(est_tags[:estimated_tagscount[j]])
	if len(part_of_est_tags) == 0:
		print "len(part_of_est_tags): 0"
		pre = 0.
	else :
		pre = float((len(correct_answers[j] & part_of_est_tags))) / float(len(part_of_est_tags))
	if len(correct_answers[j]) == 0:
		rec = 0.
	else:
		rec = float((len(correct_answers[j] & part_of_est_tags))) / float(len(correct_answers[j]))
	precision += pre
	recall += rec
	precision_eachcount[estimated_tagscount[j]] += pre
	recall_eachcount[estimated_tagscount[j]] += rec
	if (pre + rec) == 0:
		f_measure += 0.
	else:
		f_measure += (2. * pre * rec) / (pre + rec)
		f_measure_eachcount[estimated_tagscount[j]] += (2. * pre * rec) / (pre + rec)

mean_pre = precision / float(len(estimated_tags))
mean_rec = recall / float(len(estimated_tags))
mean_f_measure = f_measure / float(len(estimated_tags))
for i in range(min_tagscount, max_tagscount + 1):
	f_measure_eachcount[i] /= count_docs_eachcount[i]
	print "tags: " + str(i) + " : " + str(f_measure_eachcount[i])
print "precision sample"
print mean_pre
print "recalls sample"
print mean_rec
print "f_measures sample"
print mean_f_measure
print "each precision"
for i in range(min_tagscount, max_tagscount + 1):
	precision_eachcount[i] /= count_docs_eachcount[i]
	print "tags: " + str(i) + " : " + str(precision_eachcount[i])
print "each reacall"
for i in range(min_tagscount, max_tagscount + 1):
	recall_eachcount[i] /= count_docs_eachcount[i]
	print "tags: " + str(i) + " : " + str(recall_eachcount[i])

# with open(f_path_estimated_result + 'precisions_rand.csv', 'ab') as f:
#	print "saving precisions"
#	csvWriter = csv.writer(f)
#	csvWriter.writerow(range(1,51))
#	csvWriter.writerow(precisions)

#with open(f_path_estimated_result + 'recalls_rand.csv', 'ab') as f:
#	print "saving recalls"
#	csvWriter = csv.writer(f)
#	csvWriter.writerow(range(1,51))
#	csvWriter.writerow(recalls)

#with open(f_path_estimated_result + 'f_measures_rand.csv', 'ab') as f:
#	print "saving f_measures"
#	csvWriter = csv.writer(f)
#	csvWriter.writerow(range(1,51))
#	csvWriter.writerow(f_measures)
