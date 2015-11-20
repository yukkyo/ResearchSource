#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
import numpy

# 全文書(約50万)に対してLDA(Collapsed Gibbs Sampling)を適用する
# 各文書推定トピック、perplexity

# corpus_by_ids_file = "../../ResearchData/After_Extract_Over20Words/corpus_by_ids0.pkl"
corpus_by_ids_file = "../../ResearchData/After_Extract_Over20Words/new_corpus_by_ids.pkl"
vocab_id_new_to_old_file = "../../ResearchData/After_Extract_Over20Words/convert_vocabs_ids_new_to_old.pkl"

# Latent Dirichlet Allocation + collapsed Gibbs sampling
# 各文書中の全単語に振られたトピック、トピック分布、各トピックの語彙分布を返す
# 各文書をidで表したものや、vocabs_to_idやvocab_doc_freqが与えられてるとする

experiment_result_file = "../../ResearchData/After_Extract_Over20Words/experiment_result/"


class LDA:
	def __init__(self, K, alpha, beta, docs, V, smartinit=False):
		print "init lda instance"
		self.K = K
		self.alpha = alpha # parameter of topics prior
		self.beta = beta   # parameter of words prior
		self.docs = docs
		self.V = V

		self.z_m_n = [] # topics of words of documents
		self.n_m_z = numpy.zeros((len(self.docs), K)) + alpha     # word count of each document and topic
		self.n_z_t = numpy.zeros((K, V)) + beta # word count of each topic and vocabulary
		self.n_z = numpy.zeros(K) + V * beta    # word count of each topic

		self.N = 0
		for m, doc in enumerate(docs):
			self.N += len(doc)
			z_n = []
			for t in doc:
				if smartinit:
					p_z = self.n_z_t[:, t] * self.n_m_z[m] / self.n_z
					z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()
				else:
					z = numpy.random.randint(0, K)
				z_n.append(z)
				self.n_m_z[m, z] += 1
				self.n_z_t[z, t] += 1
				self.n_z[z] += 1
			self.z_m_n.append(numpy.array(z_n))

		print "end init lda instalce"

	def inference(self):
		"""learning once iteration"""
		for m, doc in enumerate(self.docs):
			z_n = self.z_m_n[m]
			n_m_z = self.n_m_z[m]
			for n, t in enumerate(doc):
				# discount for n-th word t with topic z
				z = z_n[n]
				n_m_z[z] -= 1
				self.n_z_t[z, t] -= 1
				self.n_z[z] -= 1

				# sampling topic new_z for t
				p_z = self.n_z_t[:, t] * n_m_z / self.n_z
				new_z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()

				# set z the new topic and increment counters
				z_n[n] = new_z
				n_m_z[new_z] += 1
				self.n_z_t[new_z, t] += 1
				self.n_z[new_z] += 1

	def worddist(self):
		"""get topic-word distribution"""
		return self.n_z_t / self.n_z[:, numpy.newaxis]

	def perplexity(self, docs=None):
		if docs == None: docs = self.docs
		phi = self.worddist()
		log_per = 0
		N = 0
		Kalpha = self.K * self.alpha
		for m, doc in enumerate(docs):
			theta = self.n_m_z[m] / (len(self.docs[m]) + Kalpha)
			for w in doc:
				log_per -= numpy.log(numpy.inner(phi[:,w], theta))
			N += len(doc)
		return numpy.exp(log_per / N)

	# 各文書におけるトピックの分布を返す関数
	def calc_thetas(self, docs=None):
		if docs == None: docs = self.docs
		thetas = numpy.zeros((len(self.docs), self.K))
		# Kalpha = self.K * self.alpha
		for m, doc in enumerate(docs):
			# doc_topic_dist[m] = self.n_m_z[m] / (len(self.docs[m]) + Kalpha)
			thetas[m] = self.n_m_z[m] / self.n_m_z[m].sum()
		return thetas

	# 各文書における各単語に振ったトピックの一覧を返す関数
	def gettopics(self):
		return self.z_m_n

def lda_learning(lda, iteration):
	pre_perp = lda.perplexity()
	perplexities = []
	print "initial perplexity=%f" % pre_perp
	for i in xrange(iteration):
		lda.inference()
		print "iteration: " + str(i)
		perp = lda.perplexity()
		perplexities.append(perp)
		print "-%d p=%f" % (i + 1, perp)
		if pre_perp:
			if pre_perp < perp:
				# output_word_topic_dist(lda, id_to_vocab)
				pre_perp = None
			else:
				pre_perp = perp
	# output_word_topic_dist(lda, id_to_vocab)
	return lda.gettopics(), perplexities

# def lda_learning(lda, iteration, id_to_vocab):
# 	pre_perp = lda.perplexity()
# 	print "initial perplexity=%f" % pre_perp
# 	for i in range(iteration):
# 		lda.inference()
# 		print "iteration: " + str(i)
# 		perp = lda.perplexity()
# 		print "-%d p=%f" % (i + 1, perp)
# 		if pre_perp:
# 			if pre_perp < perp:
# 				# output_word_topic_dist(lda, id_to_vocab)
# 				pre_perp = None
# 			else:
# 				pre_perp = perp
# 	# output_word_topic_dist(lda, id_to_vocab)
# 	# return thetas

def output_word_topic_dist(lda):
	zcount = numpy.zeros(lda.K, dtype=int)
	wordcount = [dict() for k in xrange(lda.K)]
	for xlist, zlist in zip(lda.docs, lda.z_m_n):
		for x, z in zip(xlist, zlist):
			zcount[z] += 1
			if x in wordcount[z]:
				wordcount[z][x] += 1
			else:
				wordcount[z][x] = 1

	phi = lda.worddist()
	for k in xrange(lda.K):
		print "\n-- topic: %d (%d words)" % (k, zcount[k])
		for w in numpy.argsort(-phi[k])[:20]:
			print "%s: %f (%d)" % (id_to_vocab[w], phi[k,w], wordcount[k].get(w,0))

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
	parser.add_option("-s", dest="smartinit", action="store_true", help="smart initialize of parameters", default=False)
	parser.add_option("--seed", dest="seed", type="int", help="random seed")
	(options, args) = parser.parse_args()

	# コーパスの読み込み
	# ここでのコーパスとは、各文書のリストであり、さらに各文書は語彙idを要素とするリスト
	# 低頻度や高頻度の単語(stop word などの)削除は、このソースコードでは行わないとする
	corpus = None
	with open(corpus_by_ids_file, 'rb') as f:
		print "loading corpus: " + corpus_by_ids_file
		corpus = cPickle.load(f)
		print "reduce corpus to corpus[:100000]"
		corpus = corpus[:100000]
		# test
		print "loading end"

	# id_to_vocabの読み込み
	id_to_vocab = None
	with open(vocab_id_new_to_old_file, 'rb') as f:
		print "loading id_to_vocab: " + vocab_id_new_to_old_file
		id_to_vocab = cPickle.load(f)
		print "len(vocab_id_new_to_old)" + str(len(id_to_vocab))
		print "loading end"

	# 乱数のシード設定
	if options.seed != None:
		numpy.random.seed(options.seed)

	len_id_to_vocab = len(id_to_vocab)
	id_to_vocab = None
	# LDAの初期設定
	# lda = LDA(options.K, options.alpha, options.beta, corpus, len(id_to_vocab), options.smartinit)
	# print "corpus=%d, words=%d, K=%d, a=%f, b=%f" % (len(corpus), len(id_to_vocab), options.K, options.alpha, options.beta)
	lda = LDA(options.K, options.alpha, options.beta, corpus, len_id_to_vocab, options.smartinit)
	print "corpus=%d, words=%d, K=%d, a=%f, b=%f" % (len(corpus), len_id_to_vocab, options.K, options.alpha, options.beta)


	# 推論(指定回数分回したら文書-トピック分布を返す)
	# lda_learning(lda, options.iteration, id_to_vocab)
	all_topics, perplexities = lda_learning(lda, options.iteration)
	print "all_topics[5000]"
	print all_topics[5000]
	for topic in all_topics[5000]:
		print topic
	# 必要であれば保存する
	file_name_topics = experiment_result_file + "K" + str(options.K) + 'a' + str(options.alpha) + 'b' + str(options.beta) + 'i' + str(options.iteration) + '_topics.pkl'
	with open(file_name_topics , 'wb') as f:
		print "open for saving: " + file_name_topics
		cPickle.dump(all_topics, f, cPickle.HIGHEST_PROTOCOL)
	print "save end!"

	file_name_perps = experiment_result_file + "K" + str(options.K) + 'a' + str(options.alpha) + 'b' + str(options.beta) + 'i' + str(options.iteration) + '_perps.pkl'
	with open(file_name_perps , 'wb') as f:
		print "open for saving: " + file_name_perps
		cPickle.dump(perplexities, f, cPickle.HIGHEST_PROTOCOL)
	print "save end!"
if __name__ == "__main__":
	main()
