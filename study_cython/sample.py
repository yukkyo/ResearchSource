#!/usr/bin/env python
# -*- coding: utf-8 -*-

import LDA
import numpy

class sample:
	def do1(self):
		self.alpha = 1
	def do2(self):
		self.beta = 2
	def printdo(self):
		print self.alpha
		print self.beta

docs = numpy.array([[0,1],[2,3,4],[5,6,7,8],[9,1]])
# docs = numpy.array([[0,1],[2,2],[3,3]])
lda = LDA.LDA(2, 0.5, 0.5, docs, 10)
lda.initialize_topics()
print lda.docs
print lda.z_m_n
print "-----"
print "n_z_t"
print lda.n_z_t
print "-----"
print "n_z"
print lda.n_z
print "infernce start"
lda.inference()
print lda.z_m_n
lda.inference()
print lda.z_m_n
lda.inference()
print lda.z_m_n
lda.inference()
print lda.z_m_n
lda.inference()
print lda.z_m_n