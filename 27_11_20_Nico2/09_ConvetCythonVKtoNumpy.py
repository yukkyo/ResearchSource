#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import LDA_C
# NumpyでVKMatrixを作る

f_id_to_vocab = "../../ResearchData/Experiment2/after_convert_id/list_id_vocab.pkl"
fpath_exp_result = "../../ResearchData/Experiment2/after_LDA/"

def main():
	import optparse
	import cPickle

	# オプションの読み込み
	parser = optparse.OptionParser()
	parser.add_option("--alpha", dest="alpha", type="float", help="parameter alpha", default=0.5)
	parser.add_option("--beta", dest="beta", type="float", help="parameter beta", default=0.5)
	parser.add_option("-k", dest="K", type="int", help="number of topics", default=20)
	parser.add_option("-i", dest="iteration", type="int", help="iteration count", default=100)
	parser.add_option("--seed", dest="seed", type="int", help="random seed")
	(options, args) = parser.parse_args()

	# vocab_sizeの取得
	vocabs_size = 0
	with open(f_id_to_vocab, 'rb') as f:
		print "loading id_to_vocab: " + f_id_to_vocab
		vocabs = cPickle.load(f)
		vocabs_size = len(vocabs)
		print "vocabs_size" + str(vocabs_size)
		print "loading end"

	# コーパス(cdef で作ったもの)の読み込み
	f_result = fpath_exp_result + "k" + str(options.K) + 'a' + str(options.alpha) + 'b' + str(options.beta) + 'i' + str(options.iteration)

	# with shelve.open(f_result) as dic:
	# 	print "open shelve dic for saving: " + f_result
	# 	dic['LDA'] = lda
	# 	# dic['perplexities'] = perplexities
	# 	# dic['thetas'] = thetas
	# 	# dic['vocab_topic_matrix'] = vocab_topic_matrix
	# print "save end!"

	with open(f_result + '.pkl', 'wb') as f:
		print "open for saving: " + f_result + '.pkl'
		cPickle.dump(lda, f, cPickle.HIGHEST_PROTOCOL)
		print "saving is end"


if __name__ == "__main__":
	main()