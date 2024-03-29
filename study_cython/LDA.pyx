#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: profile=True, boundscheck=False, wraparound=False

from __future__ import division
import numpy as np
cimport numpy as np
cimport cython
from libc.stdlib cimport rand, RAND_MAX
INT = np.int
ctypedef np.int_t INT_t
DOUBLE = np.float64
ctypedef np.float64_t DOUBLE_t
from libcpp.vector cimport vector

# Latent Dirichlet Allocation + collapsed Gibbs sampling
# 全文書(約50万)に対してLDA(Collapsed Gibbs Sampling)を適用する

cdef class LDA:
	def __init__(self, n_topics, alpha, beta, docs, V, iteration):
		self.n_topics = n_topics
		self.alpha = alpha # parameter of topics prior
		# これをベクトルにする？
		self.beta = beta   # parameter of words prior
		self.docs = docs
		self.V = V         # size of vocabulary
		self.iteration = iteration # iteration of 
		print "end lda instance"

	@cython.cdivision(True)
	def initialize_topics(self):
		print "initalize topics"
		cdef vector[vector[int]] docs = self.docs
		cdef int n_corpus, len_doc, m, n, new_z, v
		cdef double n_topics = self.n_topics
		cdef np.ndarray[DOUBLE_t, ndim=1] p_z
		cdef double alpha = self.alpha
		cdef double beta = self.beta
		cdef double V = self.V
		# number of times topic z and word w co-occur
		cdef int max_docs = self.docs.size()
		# word count of each document and topicl
		cdef np.ndarray[np.double_t, ndim=2] n_m_z
		n_m_z = np.zeros([max_docs, self.n_topics], dtype=np.double) + alpha
		# word count of each topic and vocabulary
		cdef np.ndarray[np.double_t, ndim=2] n_z_t
		n_z_t = np.zeros([self.n_topics, <int>V], dtype=np.double)
		n_z_t += beta
		# word count of each topic
		cdef np.ndarray[np.double_t, ndim=1] n_z
		n_z = np.zeros(n_topics_int, dtype=np.double)
		n_z += V * beta
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
		return

	@cython.cdivision(True)
	def inference(self):
		"""learning once iteration"""
		cdef vector[vector[int]] docs = self.docs
		cdef int max_docs = docs.size()
		cdef int len_doc, m, n, v, new_z, ite, ite_max
		ite_max = self.iteration
		cdef np.ndarray[np.double_t, ndim=1] p_z
		cdef np.ndarray[np.double_t, ndim=2] n_z_t = self.n_z_t
		self.n_z_t = None
		cdef np.ndarray[np.double_t, ndim=1] n_z = self.n_z
		self.n_z = None
		cdef np.ndarray[np.double_t, ndim=2] n_m_z = self.n_m_z
		self.n_m_z = None
		cdef np.ndarray[np.double_t, ndim=1] tmp_n_m_z
		cdef np.ndarray[np.double_t, ndim=1] tmp_n_z_t
		cdef vector[vector[int]] z_m_n = self.z_m_n
		cdef vector[int] z_n

		# calc first perps

		# iteration
		for ite in xrange(ite_max):
			print "ite start : " + str(ite)
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
					p_z /= p_z.sum(axis=0)
					new_z = np.random.multinomial(1, p_z).argmax()

					# set z the new topic and increment counters
					z_n[n] = new_z
					tmp_n_m_z[new_z] += 1
					n_z_t[new_z, v] += 1
					n_z[new_z] += 1

				z_m_n[m] = z_n
				n_m_z[m] = tmp_n_m_z
			# calc iteration

		self.n_z_t = n_z_t
		# self.n_z = n_z
		# self.n_m_z = n_m_z
		self.z_m_n = z_m_n
		return

	# @cython.cdivision(True)
	# def inference(self):
	# 	"""learning once iteration"""
	# 	cdef vector[vector[int]] docs = self.docs
	# 	cdef int max_docs = docs.size()
	# 	cdef int len_doc, m, n, v, new_z
	# 	cdef np.ndarray[np.double_t, ndim=1] p_z
	# 	cdef np.ndarray[np.double_t, ndim=2] n_z_t = self.n_z_t
	# 	cdef np.ndarray[np.double_t, ndim=1] n_z = self.n_z
	# 	cdef np.ndarray[np.double_t, ndim=2] n_m_z = self.n_m_z
	# 	cdef np.ndarray[np.double_t, ndim=1] tmp_n_m_z
	# 	cdef np.ndarray[np.double_t, ndim=1] tmp_n_z_t
	# 	cdef vector[vector[int]] z_m_n = self.z_m_n
	# 	cdef vector[int] z_n

	# 	cdef vector[double] p_z2
	# 	cdef int j
	# 	cdef int n_topics = self.n_topics
	# 	cdef double p_z2j, sum_p_z
	# 	cdef double u

	# 	for m in xrange(max_docs):
	# 		len_doc = docs[m].size()
	# 		for n in xrange(len_doc):
	# 			v = docs[m][n]
	# 			# discount for n-th word n with topic z
	# 			z = z_m_n[m][n]
	# 			n_m_z[m, z] -= 1
	# 			n_z_t[z, v] -= 1
	# 			n_z[z] -= 1

	# 			# sampling topic new_z for n
	# 			# どうせなら行列演算も全部for文書いた方がよい？
	# 			# tmp_n_z_t = n_z_t[:, v]
	# 			# p_z = tmp_n_z_t * n_m_z[m] / n_z
	# 			# p_z /= p_z.sum(axis=0)
	# 			# new_z = np.random.multinomial(1, p_z).argmax()

	# 			# sampling 2
	# 			p_z2.clear()
	# 			for j in xrange(n_topics):
	# 				p_z2j = n_z_t[j, v] * n_m_z[m, j] / n_z[j]
	# 				if j != 0:
	# 					p_z2j += p_z2[j-1]
	# 				p_z2.push_back(p_z2j)
	# 			u = (rand()/(RAND_MAX +1.)) * p_z2[n_topics - 1]
	# 			new_z = n_topics - 1
	# 			for j in xrange(n_topics):
	# 				if u < p_z2[j]:
	# 					new_z = j
	# 					break

	# 			# set z the new topic and increment counters
	# 			z_m_n[m][n] = new_z
	# 			n_m_z[m, new_z] += 1
	# 			n_z_t[new_z, v] += 1
	# 			n_z[new_z] += 1
	# 		if m % 100000 == 0:
	# 			print "end docs: " + str(m)
	# 	self.n_z_t = n_z_t
	# 	self.n_z = n_z
	# 	self.n_m_z = n_m_z
	# 	self.z_m_n = z_m_n
	# 	return



	# def worddist(self):
	# 	"""get topic-word distribution"""
	# 	return self.n_z_t / self.n_z[:, np.newaxis]

	# def perplexity(self):
	# 	print "calc perp" 
	# 	cdef vector[vector[int]] docs = self.docs
	# 	cdef int max_docs = docs.size()
	# 	cdef int len_doc, m, n, v, new_z
	# 	cdef double log_per = 0.
	# 	cdef double tmp_logper
	# 	cdef double Kalpha = self.n_topics * self.alpha
	# 	cdef np.ndarray[np.double_t, ndim=2] n_m_z = self.n_m_z
	# 	cdef np.ndarray[np.double_t, ndim=2] phi
	# 	phi = self.worddist()
	# 	cdef np.ndarray[np.double_t, ndim=1] tmp_phi
	# 	cdef np.ndarray[np.double_t, ndim=2] theta

	# 	for m in xrange(max_docs):
	# 		len_doc = docs[m].size()
	# 		theta = n_m_z[m] / (len_doc + Kalpha)
	# 		for n in xrange(len_doc):
	# 			v = docs[m][n]
	# 			tmp_phi = phi[:,v]
	# 			tmp_logper = np.dot(tmp_phi, theta)
	# 			log_per -= np.log(tmp_logper)
	# 	return np.exp(log_per / self.n_corpus)

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