#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: profile=True, boundscheck=False, wraparound=False

from __future__ import division
import numpy as np
cimport numpy as np
cimport cython
from libc.stdlib cimport rand, RAND_MAX
DTYPE = np.int
ctypedef np.int_t DTYPE_t
from libcpp.vector cimport vector
from libc.math cimport log, exp

# Latent Dirichlet Allocation + collapsed Gibbs sampling
# 全文書(約50万)に対してLDA(Collapsed Gibbs Sampling)を適用する
# トピック-語彙分布行列の各値からBetaを引いて転置した語彙-トピック分布、perplexitiesを返す

class LDA:
	# @cython.boundschecnk(False)
	# @cython.wraparound(False)
	@cython.cdivision(True)
	def __init__(self, r_n_topics, r_alpha, r_beta, raw_docs, r_V, r_iteration):
		print "init lda instance"
		self.n_topics = r_n_topics
		self.alpha = r_alpha # parameter of topics prior
		self.beta = r_beta   # parameter of words prior
		self.V = r_V         # size of vocabulary
		self.perps = []
		self.iteration = r_iteration
		print "initalize topics"
		cdef vector[vector[long]] docs = raw_docs
		self.docs = docs
		print "end lda instance"
		cdef int n_corpus, len_doc, m, n, new_z, v
		n_corpus = 0
		cdef int n_topics_int = self.n_topics
		cdef double n_topics = self.n_topics
		cdef double alpha = self.alpha
		cdef double beta = self.beta
		cdef double V = self.V
		cdef double Vbeta = V * beta
		n_topics_s = self.n_topics
		v2 = self.V
		# number of times topic z and word w co-occur
		cdef int max_docs = 1
		max_docs = docs.size()
		# word count of each document and topic
		cdef vector[vector[double]] n_m_z
		n_m_z = vector[vector[double]](max_docs, vector[double](n_topics_int, alpha))
		# word count of each topic and vocabulary
		cdef vector[vector[double]] n_z_t
		n_z_t = vector[vector[double]](n_topics_int, vector[double](<int>V, beta))
		# word count of each topic
		cdef vector[double] n_z
		n_z = vector[double](n_topics_int, Vbeta)

		cdef vector[vector[int]] z_m_n
		cdef vector[int] z_n

		for m in xrange(max_docs):
			len_doc = docs[m].size()
			n_corpus += len_doc
			z_n.clear()
			for n in xrange(len_doc):
				v = docs[m][n]
				new_z = int((rand()/(RAND_MAX +1.)) * n_topics)
				z_n.push_back(new_z)
				n_m_z[m][new_z] += 1.
				n_z_t[new_z][v] += 1.
				n_z[new_z] += 1
			z_m_n.push_back(z_n)
			if (m - 1) % 100000 == 0:
				print "end docs: " + str(m)

		self.n_corpus = n_corpus
		self.n_m_z = n_m_z
		self.n_z_t = n_z_t
		self.n_z = n_z
		self.z_m_n = z_m_n # topics of words of documents
		print "end initialize topics"
		return

	@cython.cdivision(True)
	def inference(self):
		"""learning once iteration"""
		print "inference start"
		cdef vector[vector[long]] docs = self.docs
		cdef int max_docs = docs.size()
		cdef int len_doc, n, new_z, j, ite, iteration
		iteration = self.iteration
		cdef long v, m
		cdef int n_topics = self.n_topics
		cdef vector[vector[double]] n_z_t = self.n_z_t
		cdef vector[vector[double]] n_m_z = self.n_m_z
		cdef vector[double] n_m_z_m
		n_m_z_m.resize(n_topics)
		cdef vector[vector[int]] z_m_n = self.z_m_n
		cdef vector[double] n_z = self.n_z
		cdef vector[int] z_n
		cdef vector[int] z_m_n_m
		cdef vector[double] p_z2
		p_z2.resize(n_topics)
		cdef double p_z2j, u, perp
		cdef long V = self.V
		cdef double alpha = self.alpha
		cdef long n_corpus = self.n_corpus

		print "calc first perp"
		perp = self.perplexity(docs, n_topics, n_m_z,
									n_z_t, n_z, V, alpha, n_corpus)
		print "perp: " + str(perp)
		self.perps.append(perp)

		for ite in xrange(iteration):
			print "ite: " + str(ite)
			# sampling each word in corpus
			for m in xrange(max_docs):
				len_doc = docs[m].size()
				n_m_z_m = n_m_z[m]
				z_m_n_m = z_m_n[m]
				for n in xrange(len_doc):
					v = docs[m][n]
					# discount for n-th word n with topic z
					z = z_m_n_m[n]
					n_m_z_m[z] -= 1
					n_z_t[z][v] -= 1
					n_z[z] -= 1

					# sampling new_z
					for j in xrange(n_topics):
						p_z2j = n_z_t[j][v] * n_m_z_m[j]
						p_z2j /= n_z[j]
						if j != 0:
							p_z2j += p_z2[j-1]
						p_z2[j] = p_z2j
					u = (rand()/(RAND_MAX +1.))
					u *= p_z2[n_topics - 1]
					new_z = n_topics - 1
					for j in xrange(n_topics):
						if u < p_z2[j]:
							new_z = j
							break

					# set z the new topic and increment counters
					z_m_n_m[n] = new_z
					n_m_z_m[new_z] += 1
					n_z_t[new_z][v] += 1
					n_z[new_z] += 1

				z_m_n[m] = z_m_n_m
				n_m_z[m] = n_m_z_m
				if (m - 1) % 100000 == 0:
					print "end docs: " + str(m)

			perp = self.perplexity(docs, n_topics, n_m_z,
									n_z_t, n_z, V, alpha, n_corpus)
			print "perp: " + str(perp)
			self.perps.append(perp)

		self.n_z_t = n_z_t
		self.n_z = n_z
		self.n_m_z = n_m_z
		self.z_m_n = z_m_n
		return

	# def worddist(self):
	# 	"""get topic-word distribution"""
	# 	return self.n_z_t / self.n_z[:, np.newaxis]

	@cython.cdivision(True)
	def perplexity( self,
					vector[vector[long]] docs,
					int n_topics,
					vector[vector[double]] n_m_z,
					vector[vector[double]] n_z_t,
					vector[double] n_z,
					int V,
					double alpha,
					long n_corpus
					):
		print "calc init" 
		cdef vector[long] docs_m
		cdef int max_docs = docs.size()
		cdef int len_doc, m, n, v, j
		cdef double n_z_j
		cdef vector[double] theta
		cdef double Kalpha = <double>n_topics * alpha
		cdef double log_per = 0.
		cdef double tmp_logper
		cdef double len_doc_kalpha

		print "calc phi"
		for j in xrange(n_topics):
			n_z_j = n_z[j]
			for v in xrange(V):
				n_z_t[j][v] /= n_z_j
		print "calc perp"
		for m in xrange(max_docs):
			len_doc = docs[m].size()
			len_doc_kalpha = <double>len_doc + Kalpha
			theta = n_m_z[m]
			docs_m = docs[m]
			for j in xrange(n_topics):
				theta[j] = theta[j] / len_doc_kalpha

			for n in xrange(len_doc):
				v = docs_m[n]
				tmp_logper = 0.0
				for j in xrange(n_topics):
					tmp_logper += (theta[j] * n_z_t[j][v])
				log_per -= log(tmp_logper)
		log_per /= <double>n_corpus
		return exp(log_per)

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