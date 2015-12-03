#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: profile=True, boundscheck=False, wraparound=False

import numpy as np
cimport numpy as np
cimport cython
DTYPE = np.int
ctypedef np.int_t DTYPE_t
from libcpp.vector cimport vector

# Latent Dirichlet Allocation + collapsed Gibbs sampling
# 全文書(約50万)に対してLDA(Collapsed Gibbs Sampling)を適用する
# トピック-語彙分布行列の各値からBetaを引いて転置した語彙-トピック分布、perplexitiesを返す

class LDA:
	# @cython.boundschecnk(False)
	# @cython.wraparound(False)
	def __init__(self, double n_topics, double alpha, double beta,
									vector[vector[int]] docs, double V):
		print "init lda instance"
		self.n_topics = n_topics
		self.alpha = alpha # parameter of topics prior
		self.beta = beta   # parameter of words prior
		self.docs = docs
		self.V = V         # size of vocabulary
		print "end lda instance"

	def initialize_topics(self):
		print "initalize topics"
		cdef vector[vector[int]] docs = self.docs
		cdef int n_corpus, len_doc, m, n, new_z, v
		cdef np.ndarray[np.double_t, ndim=1] p_z
		# number of times topic z and word w co-occur
		cdef np.ndarray[np.double_t, ndim=2] n_z_t = np.zeros((self.n_topics, self.V), dtype=np.double) + self.alpha
		cdef np.ndarray[np.double_t, ndim=1] n_z = np.zeros(self.n_topics, dtype=np.double) + self.V * self.beta
		cdef int max_docs = docs.size()
		cdef np.ndarray[np.double_t, ndim=2] n_m_z = np.zeros((max_docs, self.n_topics), dtype=np.double)
		cdef vector[vector[int]] z_m_n
		cdef vector[int] z_n

		for m in xrange(max_docs):
			len_doc = docs[m].size()
			n_corpus += len_doc
			z_n.clear()
			for n in xrange(len_doc):
				v = docs[m][n]
				new_z = np.random.randint(0, self.n_topics)
				z_n.push_back(new_z)
				n_m_z[m, new_z] += 1
				n_z_t[new_z, v] += 1
				n_z[new_z] += 1
			z_m_n.push_back(z_n)
			if m % 100000 == 0:
				print "end docs: " + str(m)

		self.n_corpus = n_corpus
		self.n_m_z = n_m_z
		self.n_z_t = n_z_t
		self.n_z = n_z
		self.z_m_n = z_m_n # topics of words of documents
		print "end initialize topics"

	def inference(self):
		"""learning once iteration"""
		cdef vector[vector[int]] docs = self.docs
		cdef int max_docs = docs.size()
		cdef int len_doc, m, n, v, new_z
		cdef np.ndarray[np.double_t, ndim=1] p_z
		cdef np.ndarray[np.double_t, ndim=2] n_z_t = self.n_z_t
		cdef np.ndarray[np.double_t, ndim=1] n_z = self.n_z
		cdef np.ndarray[np.double_t, ndim=2] n_m_z = self.n_m_z
		cdef np.ndarray[np.double_t, ndim=1] tmp_n_m_z
		cdef np.ndarray[np.double_t, ndim=1] tmp_n_z_t
		cdef vector[vector[int]] z_m_n = self.z_m_n
		cdef vector[int] z_n

		for m in xrange(max_docs):
			len_doc = docs[m].size()
			z_n = z_m_n[m]
			tmp_n_m_z = n_m_z[m]
			for n in xrange(len_doc):
				v = docs[m][n]
				# discount for n-th word n with topic z
				z = z_n[n]
				tmp_n_m_z[z] -= 1
				n_z_t[z, v] -= 1
				n_z[z] -= 1

				# sampling topic new_z for n
				tmp_n_z_t = n_z_t[:, v]
				p_z = tmp_n_z_t * tmp_n_m_z / n_z
				p_z /= p_z.sum()
				new_z = np.random.multinomial(1, p_z).argmax()

				# set z the new topic and increment counters
				z_n[n] = new_z
				tmp_n_m_z[new_z] += 1
				n_z_t[new_z, v] += 1
				n_z[new_z] += 1

			z_m_n[m] = z_n
			n_m_z[m] = tmp_n_m_z

		self.n_z_t = n_z_t
		self.n_z = n_z
		self.n_m_z = n_m_z
		self.z_m_n = z_m_n

	def worddist(self):
		"""get topic-word distribution"""
		return self.n_z_t / self.n_z[:, np.newaxis]

	def perplexity(self):
		cdef vector[vector[int]] docs = self.docs
		cdef int max_docs = docs.size()
		cdef int len_doc, m, n, v, new_z
		cdef double log_per = 0.
		cdef double tmp_logper
		cdef double Kalpha = self.n_topics * self.alpha
		cdef np.ndarray[np.double_t, ndim=2] n_m_z = self.n_m_z
		cdef np.ndarray[np.double_t, ndim=2] phi
		phi = self.worddist()
		cdef np.ndarray[np.double_t, ndim=1] tmp_phi
		cdef np.ndarray[np.double_t, ndim=2] theta

		for m in xrange(max_docs):
			len_doc = docs[m].size()
			theta = n_m_z[m] / (len_doc + Kalpha)
			for n in xrange(len_doc):
				v = docs[m][n]
				tmp_phi = phi[:,v]
				tmp_logper = np.dot(tmp_phi, theta)
				log_per -= np.log(tmp_logper)
		return np.exp(log_per / self.n_corpus)




		# docs = self.docs
		# phi = self.worddist()
		# log_per = 0
		# N = 0
		# Kalpha = self.n_topics * self.alpha
		# for m, doc in enumerate(docs):
		# 	theta = self.n_m_z[m] / (len(self.docs[m]) + Kalpha)
		# 	for w in doc:
		# 		log_per -= np.log(np.dot(phi[:,w], theta))
		# 	N += len(doc)
		# return np.exp(log_per / N)

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