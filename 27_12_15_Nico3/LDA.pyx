#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: profile=True, boundscheck=False, wraparound=False

from __future__ import division
cimport cython
from libc.stdlib cimport rand, RAND_MAX
from libcpp.vector cimport vector
from libc.math cimport log, exp
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

# Latent Dirichlet Allocation + collapsed Gibbs sampling
# 全文書(約50万)に対してLDA(Collapsed Gibbs Sampling)を適用する
# トピック-語彙分布行列の各値からBetaを引いて転置した語彙-トピック分布、perplexitiesを返す

class LDA:
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
		cdef vector[vector[int]] docs = raw_docs
		# self.docs = docs
		cdef int n_corpus, len_doc, m, n, new_z, v
		n_corpus = 0
		cdef int n_topics_int = self.n_topics
		cdef int V_int = self.V
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
		# n_z_t = vector[vector[double]](n_topics_int, vector[double](<int>V, beta))
		n_z_t = vector[vector[double]](V_int, vector[double](n_topics_int, beta))
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
				n_z_t[v][new_z] += 1.
				n_z[new_z] += 1
			z_m_n.push_back(z_n)
		print "end initialize topics"

		"""learning once iteration"""
		print "inference start"
		cdef int j, ite, iteration
		iteration = self.iteration
		cdef vector[vector[double]] n_z_t_tmp
		cdef vector[double] n_m_z_m
		n_m_z_m.resize(n_topics_int)
		cdef vector[int] z_m_n_m
		cdef vector[double] p_z2
		p_z2.resize(n_topics_int)
		cdef double p_z2j, u, perp
		# cdef long V = self.V
		cdef vector[int] docs_m
		cdef double n_z_j
		cdef vector[double] theta
		cdef double Kalpha = <double>n_topics * alpha
		cdef double log_per, tmp_logper, len_doc_kalpha

		print "calc first perp"
		n_z_t_tmp = n_z_t
		log_per = 0.0
		for v in xrange(V_int):
			for j in xrange(n_topics_int):
				n_z_t_tmp[v][j] /= n_z[j]

		for m in xrange(max_docs):
			len_doc = docs[m].size()
			len_doc_kalpha = <double>len_doc + Kalpha
			theta = n_m_z[m]
			docs_m = docs[m]
			for j in xrange(n_topics_int):
				theta[j] = theta[j] / len_doc_kalpha

			for n in xrange(len_doc):
				v = docs_m[n]
				tmp_logper = 0.0
				for j in xrange(n_topics_int):
					tmp_logper += (theta[j] * n_z_t_tmp[v][j])
				log_per -= log(tmp_logper)
		theta.clear()
		n_z_t_tmp.clear()
		log_per /= <double>n_corpus
		perp = exp(log_per)
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
					n_z_t[v][z] -= 1
					n_z[z] -= 1

					# sampling new_z
					for j in xrange(n_topics_int):
						p_z2j = n_z_t[v][j] * n_m_z_m[j]
						p_z2j /= n_z[j]
						if j != 0:
							p_z2j += p_z2[j-1]
						p_z2[j] = p_z2j
					u = (rand()/(RAND_MAX +1.))
					u *= p_z2[n_topics_int - 1]
					new_z = n_topics_int - 1
					for j in xrange(n_topics_int):
						if u < p_z2[j]:
							new_z = j
							break

					# set z the new topic and increment counters
					z_m_n_m[n] = new_z
					n_m_z_m[new_z] += 1
					n_z_t[v][new_z] += 1
					n_z[new_z] += 1

				z_m_n[m] = z_m_n_m
				n_m_z[m] = n_m_z_m
				if (m + 1) % 100000 == 0:
					print "end docs: " + str(m + 1)

			print "calc perp"
			log_per = 0.0
			n_z_t_tmp = n_z_t
			for v in xrange(V_int):
				for j in xrange(n_topics_int):
					n_z_t_tmp[v][j] /= n_z[j]
			for m in xrange(max_docs):
				len_doc = docs[m].size()
				len_doc_kalpha = <double>len_doc + Kalpha
				theta = n_m_z[m]
				docs_m = docs[m]
				for j in xrange(n_topics_int):
					theta[j] = theta[j] / len_doc_kalpha

				for n in xrange(len_doc):
					v = docs_m[n]
					tmp_logper = 0.0
					for j in xrange(n_topics_int):
						tmp_logper += (theta[j] * n_z_t_tmp[v][j])
					log_per -= log(tmp_logper)
			theta.clear()
			n_z_t_tmp.clear()
			log_per /= <double>n_corpus
			perp = exp(log_per)
			print "perp: " + str(perp)
			self.perps.append(perp)

			print "calc new alpha and beta"

		self.n_z_t = n_z_t
		self.z_m_n = z_m_n
		return