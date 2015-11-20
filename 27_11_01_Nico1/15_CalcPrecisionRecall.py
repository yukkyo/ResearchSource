#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import numpy
import csv

# テストデータcorpus[100000:110000]に対してタグを50個まで推薦する

# corpus_by_ids_file = "../../ResearchData/After_Extract_Over20Words/corpus_by_ids0.pkl"
# vocab_doc_freq_file = "../../ResearchData/After_Extract_Over20Words/vocab_doc_freq0.pkl"
id_to_vocab_file = "../../ResearchData/After_Extract_Over20Words/list_id_to_vocab0.pkl"

# corpus_by_ids_over10count_file = "../../ResearchData/After_Extract_Over20Words/corpus_by_ids_over10count.pkl"
vocabs_ids_over10count_file = "../../ResearchData/After_Extract_Over20Words/vocabs_ids_over10count.pkl"

new_corpus_by_ids_file = "../../ResearchData/After_Extract_Over20Words/new_corpus_by_ids.pkl"
f_convert_vocaid_old_to_new = "../../ResearchData/After_Extract_Over20Words/convert_vocabs_ids_old_to_new.pkl"
f_convert_vocaid_new_to_old = "../../ResearchData/After_Extract_Over20Words/convert_vocabs_ids_new_to_old.pkl"

experiment_result_file = "../../ResearchData/After_Extract_Over20Words/experiment_result/"

K = 100
ITERATION = 250
ALPHA = 0.1
BETA = 0.01
MAX_TRAIN_DOCS = 100000
MAX_TEST_DOCS = 1000
MAX_AUTO_TAGS_PER_DOC = 50
# corpus等の読み込み
new_corpus = None
id_to_vocab = None
vocab_topic_matrix_norm = None
vocab_topic_matrix_zero = None
ids_new_to_old = None

# # 正解タグデータ(旧id)を作る
f_old_corpus = "../../ResearchData/After_Extract_Over20Words/corpus_by_ids0.pkl"
f_id_to_vocab = "../../ResearchData/After_Extract_Over20Words/list_id_to_vocab0.pkl"
old_corpus = None
test_old_corpus = None
with open(f_old_corpus, 'rb') as f:
	print "loading: " + f_old_corpus
	old_corpus = cPickle.load(f)
	test_old_corpus = old_corpus[MAX_TRAIN_DOCS : MAX_TRAIN_DOCS + MAX_TEST_DOCS]

print "len(old_corpus): " + str(len(old_corpus))
print "len(test_old_corpus)" + str(len(test_old_corpus))

with open(f_id_to_vocab, 'rb') as f:
	print "loading: " + f_id_to_vocab
	id_to_vocab = cPickle.load(f)

print "make correct_answers"
correct_answers = [set([v_id for v_id in d if id_to_vocab[v_id].find('___') == 0]) for d in test_old_corpus]

# test correct_answers
# for i in range(10):
# 	print "doc: " + str(500 + i) 
# 	for ans in correct_answers[500 + i]:
# 		print id_to_vocab[ans]

# # 推薦したタグを昔のidに変換する
estimated_tags = None
f_result_tags = experiment_result_file + "K" + str(K) + 'a' + str(ALPHA) + 'b' + str(BETA) + 'i' + str(ITERATION) + '_result_tags.pkl'
with open(f_result_tags, 'rb') as f:
	print "loading: " + f_result_tags
	estimated_tags = cPickle.load(f)
	print "len(estimated_tags): " + str(len(estimated_tags))

vocaid_to_old = None
with open(f_convert_vocaid_new_to_old) as f:
	print "loading: " + f_convert_vocaid_new_to_old
	vocaid_to_old = cPickle.load(f)

print "convert estimated_tags to oldid"
estimated_tags_oldid = [[vocaid_to_old[tag] for tag in tags] for tags in estimated_tags]

# 推薦するタグの個数を変えて、precision、recall、f-measureを出す
precisions = []
recalls = []
f_measures = []
print "calc precision, recall, f-measure"
for i in range(MAX_AUTO_TAGS_PER_DOC):
	precision = 0.
	recall = 0.
	f_measure = 0.
	for j, est_tags in enumerate(estimated_tags_oldid):
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
	mean_pre = precision / float(len(estimated_tags_oldid))
	mean_rec = recall / float(len(estimated_tags_oldid))
	mean_f_measure = f_measure / float(len(estimated_tags_oldid))
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

with open('precisions.csv', 'ab') as f:
	print "saving precisions"
	csvWriter = csv.writer(f)
	csvWriter.writerow(range(1,51))
	csvWriter.writerow(precisions)

with open('recalls.csv', 'ab') as f:
	print "saving recalls"
	csvWriter = csv.writer(f)
	csvWriter.writerow(range(1,51))
	csvWriter.writerow(recalls)

with open('f_measures.csv', 'ab') as f:
	print "saving f_measures"
	csvWriter = csv.writer(f)
	csvWriter.writerow(range(1,51))
	csvWriter.writerow(f_measures)