#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import numpy
# import LDA
import LDA_C
import time
# Latent Dirichlet Allocation + collapsed Gibbs sampling
# 全文書(約50万)に対してLDA(Collapsed Gibbs Sampling)を適用する
# トピック-語彙分布行列の各値からBetaを引いて転置した語彙-トピック分布、perplexitiesを返す

f_corpus_by_ids_train = "../../ResearchData/Experiment3/after_convert_id/docs_as_id_train.pkl"
f_id_to_vocab = "../../ResearchData/Experiment3/after_convert_id/list_id_vocab.pkl"
fpath_exp_result = "../../ResearchData/Experiment3/after_LDA/"

def main():
	import optparse
	import shelve
	import cPickle

	# オプションの読み込み
	parser = optparse.OptionParser()
	parser.add_option("--alpha", dest="alpha", type="float", help="parameter alpha", default=0.5)
	parser.add_option("--beta", dest="beta", type="float", help="parameter beta", default=0.5)
	parser.add_option("-k", dest="K", type="int", help="number of topics", default=20)
	parser.add_option("-i", dest="iteration", type="int", help="iteration count", default=100)
	parser.add_option("--seed", dest="seed", type="int", help="random seed")
	(options, args) = parser.parse_args()

	# 乱数のシード設定
	if options.seed != None:
		numpy.random.seed(options.seed)

	# コーパスの読み込み
	# ここでのコーパスとは、各文書のリストであり、さらに各文書は語彙idを要素とするリスト
	corpus = None
	with open(f_corpus_by_ids_train, 'rb') as f:
		print "loading corpus_train: " + f_corpus_by_ids_train
		corpus = cPickle.load(f)
		print "loading end"

	# vocab_sizeの取得
	vocabs_size = 0
	with open(f_id_to_vocab, 'rb') as f:
		print "loading id_to_vocab: " + f_id_to_vocab
		vocabs = cPickle.load(f)
		vocabs_size = len(vocabs)
		print "vocabs_size" + str(vocabs_size)
		print "loading end"

	# LDAの初期設定
	corpus = corpus[:500000]
	print "corpus=%d, vocabs_size=%d, K=%d, a=%f, b=%f" % (len(corpus), vocabs_size, options.K, options.alpha, options.beta)
	# lda = LDA_C.LDA(options.K, options.alpha, options.beta, corpus, vocabs_size, options.iteration)
	start = time.time()
	lda = LDA_C.LDA(options.K, options.alpha, options.beta, corpus, vocabs_size, 1)
	corpus = None
	elapsed_time = time.time() - start
	print ("elapsed_time:{0}".format(elapsed_time)) + "[sec]"
	# start = time.time()
	# lda.inference()
	# elapsed_time = time.time() - start
	# print ("elapsed_time:{0}".format(elapsed_time)) + "[sec]"

	# 保存
	# f_result = fpath_exp_result + "k" + str(options.K) + 'a' + str(options.alpha) + 'b' + str(options.beta) + 'i' + str(options.iteration)
	# with open(f_result + '.pkl', 'wb') as f:
	# 	print "open for saving: " + f_result + '.pkl'
	# 	cPickle.dump(lda, f, cPickle.HIGHEST_PROTOCOL)
	# 	print "saving is end"

if __name__ == "__main__":
	main()


