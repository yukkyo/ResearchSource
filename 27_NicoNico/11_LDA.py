#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle

# 全文書(約50万)に対してLDA(Collapsed Gibbs Sampling)を適用する
# 各文書推定トピック、perplexity

vocab_to_id_file = "../../ResearchData/After_Extract_Over20Words/dic_vocab_to_id0.pkl"
corpus_by_ids_file = "../../ResearchData/After_Extract_Over20Words/corpus_by_ids0.pkl"
vocab_doc_freq_file = "../../ResearchData/After_Extract_Over20Words/vocab_doc_freq0.pkl"

