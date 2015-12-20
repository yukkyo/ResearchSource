#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy

# Latent Dirichlet Allocation + collapsed Gibbs sampling
# 全文書(約50万)に対してLDA(Collapsed Gibbs Sampling)を適用する
# トピック-語彙分布行列の各値からBetaを引いて転置した語彙-トピック分布、perplexitiesを返す

class LDA:
	def __init__(self, K, alpha, beta, docs, V):
		print "init lda instance"
		self.K = K
		self.alpha = alpha # parameter of topics prior
		self.beta = beta   # parameter of words prior
		self.docs = docs
		self.V = V         # size of vocabulary
                self.perps[]
		self.z_m_n = [] # topics of words of documents
		len_docs = len(self.docs)
		self.n_m_z = numpy.zeros((len_docs, K)) + alpha     # word count of each document and topic
		self.n_z_t = numpy.zeros((K, V)) + beta # word count of each topic and vocabulary
		self.n_z = numpy.zeros(K) + V * beta    # word count of each topic

		self.N = 0
		print "init topic for each word in corpus"
		for m, doc in enumerate(docs):
			self.N += len(doc)
			z_n = []
			for t in doc:
				# p_z = self.n_z_t[:, t] * self.n_m_z[m] / self.n_z
				# z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()
				z = numpy.random.randint(0, K)
				z_n.append(z)
				self.n_m_z[m, z] += 1
				self.n_z_t[z, t] += 1
				self.n_z[z] += 1
			self.z_m_n.append(numpy.array(z_n))
			if m % 100000 == 0:
				print "end docs: " + str(m)
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

	def perplexity(self):
		docs = self.docs
		phi = self.worddist()
		log_per = 0
		N = 0
		Kalpha = self.K * self.alpha
		for m, doc in enumerate(docs):
			theta = self.n_m_z[m] / (len(self.docs[m]) + Kalpha)
			for w in doc:
				log_per -= numpy.log(numpy.dot(phi[:,w], theta))
			N += len(doc)
		return numpy.exp(log_per / N)

	# 各文書におけるトピックの分布を返す関数
	def calc_thetas(self, docs=None):
		print "calc_thetas"
		if docs == None: docs = self.docs
		thetas = numpy.zeros((len(self.docs), self.K))
		# Kalpha = self.K * self.alpha
		for m, doc in enumerate(docs):
			# doc_topic_dist[m] = self.n_m_z[m] / (len(self.docs[m]) + Kalpha)
			thetas[m] = self.n_m_z[m] / self.n_m_z[m].sum()
		return thetas

	# 各文書における各単語に振ったトピックの一覧を返す
	def gettopics(self):
		return self.z_m_n

	# 語彙-トピック行列を返す（語彙分布からBetaを引いて転置してかけたものに等しい）
	def calc_vocab_topic_matrix(self):
		return (self.n_z_t - self.beta).T
