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
cdef extern from "<boost/math/special_functions/digamma.hpp>" namespace "boost::math":
	double digamma(double)

cdef class Sample_dig:
	@cython.cdivision(True)
	def __init__(self):
		cdef double sample_dig = digamma(0.5)
		print "sample_dig" + str(sample_dig)