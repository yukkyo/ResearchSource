#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
cimport numpy as np
cimport cython
DTYPE = np.int
ctypedef np.int_t DTYPE_t

# Latent Dirichlet Allocation + collapsed Gibbs sampling
# 全文書(約50万)に対してLDA(Collapsed Gibbs Sampling)を適用する
# トピック-語彙分布行列の各値からBetaを引いて転置した語彙-トピック分布、perplexitiesを返す

class LDA:
	# @cython.boundschecnk(False)
	# @cython.wraparound(False)
	def __init__(self, int n_topics, double alpha, double beta, 
					np.ndarray[DTYPE_t, ndim=2] docs, int V):
		print "init lda instance"
		self.n_topics = n_topics
		self.alpha = alpha # parameter of topics prior
		self.beta = beta   # parameter of words prior
		self.docs = docs
		self.V = V         # size of vocabulary
		self.z_m_n = [] # topics of words of documents
		cdef int n_docs = len(self.docs)
		self.n_corpus = 0
		cdef np.ndarray[DTYPE_t, ndim=2] nmz = np.zeros((n_docs, self.n_topics), dtype=DTYPE)
		# number of times topic z and word w co-occur
		cdef np.ndarray[DTYPE_t, ndim=2] nzt = np.zeros((self.n_topics, self.V), dtype=DTYPE) + self.alpha
		cdef np.ndarray[DTYPE_t, ndim=1] nm = np.zeros(n_docs, dtype=DTYPE) + self.beta
		cdef np.ndarray[DTYPE_t, ndim=1] nz = np.zeros(self.n_topics, dtype=DTYPE) + self.V * self.beta
		self.n_m_z = nmz
		self.n_z_t = nzt
		self.n_z = nz
		self.n_m = nm
		print "end lda instance"

	def initialize_topics(self):
		print "initalize topics"
		cdef int n_corpus = 0
		cdef int len_doc = 0
		for m, doc in enumerate(self.docs):
			len_doc = len(doc)
			n_corpus += len_doc
			self.n_m[m] = len_doc
			z_n = []
			for t in doc:
				p_z = self.n_z_t[:, t] * self.n_m_z[m] / self.n_z
				z = np.random.multinomial(1, p_z / p_z.sum()).argmax()
				# z = np.random.randint(0, n_topics)
				z_n.append(z)
				self.n_m_z[m, z] += 1
				self.n_z_t[z, t] += 1
				self.n_z[z] += 1
			self.z_m_n.append(np.array(z_n))
			if m % 100000 == 0:
				print "end docs: " + str(m)
		self.n_corpus = n_corpus
		print "end"

	# def inference(self):
	# 	"""learning once iteration"""
	# 	for m, doc in enumerate(self.docs):
	# 		z_n = self.z_m_n[m]
	# 		n_m_z = self.n_m_z[m]
	# 		for n, t in enumerate(doc):
	# 			# discount for n-th word t with topic z
	# 			z = z_n[n]
	# 			n_m_z[z] -= 1
	# 			self.n_z_t[z, t] -= 1
	# 			self.n_z[z] -= 1

	# 			# sampling topic new_z for t
	# 			p_z = self.n_z_t[:, t] * n_m_z / self.n_z
	# 			new_z = np.random.multinomial(1, p_z / p_z.sum()).argmax()

	# 			# set z the new topic and increment counters
	# 			z_n[n] = new_z
	# 			n_m_z[new_z] += 1
	# 			self.n_z_t[new_z, t] += 1
	# 			self.n_z[new_z] += 1

	# def worddist(self):
	# 	"""get topic-word distribution"""
	# 	return self.n_z_t / self.n_z[:, np.newaxis]

	# def perplexity(self):
	# 	docs = self.docs
	# 	phi = self.worddist()
	# 	log_per = 0
	# 	N = 0
	# 	Kalpha = self.n_topics * self.alpha
	# 	for m, doc in enumerate(docs):
	# 		theta = self.n_m_z[m] / (len(self.docs[m]) + Kalpha)
	# 		for w in doc:
	# 			log_per -= np.log(np.dot(phi[:,w], theta))
	# 		N += len(doc)
	# 	return np.exp(log_per / N)

	# # 各文書におけるトピックの分布を返す関数
	# def calc_thetas(self, docs=None):
	# 	print "calc_thetas"
	# 	if docs == None: docs = self.docs
	# 	thetas = np.zeros((len(self.docs), self.n_topics))
	# 	# n_topicsalpha = self.n_topics * self.alpha
	# 	for m, doc in enumerate(docs):
	# 		# doc_topic_dist[m] = self.n_m_z[m] / (len(self.docs[m]) + n_topicsalpha)
	# 		thetas[m] = self.n_m_z[m] / self.n_m_z[m].sum()
	# 	return thetas

	# # 各文書における各単語に振ったトピックの一覧を返す
	# def gettopics(self):
	# 	return self.z_m_n

	# # 語彙-トピック行列を返す（語彙分布からBetaを引いて転置してかけたものに等しい）
	# def calc_vocab_topic_matrix(self):
	# 	return (self.n_z_t - self.beta).T