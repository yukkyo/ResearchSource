#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Latent Dirichlet Allocation + collapsed Gibbs sampling
# 各文書のトピック分布を返す

import numpy

class LDA:
    def __init__(self, K, alpha, beta, docs, V, smartinit=True):
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

    # 各文書におけるトピックの確率を返す関数
    def calc_thetas(self, docs=None):
        if docs == None: docs = self.docs
        thetas = numpy.zeros((len(self.docs), self.K))
        # Kalpha = self.K * self.alpha
        for m, doc in enumerate(docs):
            # doc_topic_dist[m] = self.n_m_z[m] / (len(self.docs[m]) + Kalpha)
            thetas[m] = self.n_m_z[m] / self.n_m_z[m].sum()
        return thetas

def lda_learning(lda, iteration, voca):
    pre_perp = lda.perplexity()
    print "initial perplexity=%f" % pre_perp
    for i in range(iteration):
        lda.inference()
        print "iteration: " + str(i)
        # perp = lda.perplexity()
        # print "-%d p=%f" % (i + 1, perp)
        # if pre_perp:
        #     if pre_perp < perp:
        #         output_word_topic_dist(lda, voca)
        #         pre_perp = None
        #     else:
        #         pre_perp = perp
    output_word_topic_dist(lda, voca)
    thetas = lda.calc_thetas()
    return thetas

def output_word_topic_dist(lda, voca):
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
    # for k in xrange(lda.K):
    #     print "\n-- topic: %d (%d words)" % (k, zcount[k])
    #     for w in numpy.argsort(-phi[k])[:20]:
    #         print "%s: %f (%d)" % (voca[w], phi[k,w], wordcount[k].get(w,0))

def main():
    import optparse
    import vocabulary
    import shelve

    # オプションの読み込み
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="filename", help="corpus filename")
    # parser.add_option("-c", dest="corpus", help="using range of Brown corpus' files(start:end)")
    parser.add_option("--alpha", dest="alpha", type="float", help="parameter alpha", default=0.5)
    parser.add_option("--beta", dest="beta", type="float", help="parameter beta", default=0.5)
    parser.add_option("-k", dest="K", type="int", help="number of topics", default=20)
    parser.add_option("-i", dest="iteration", type="int", help="iteration count", default=100)
    parser.add_option("-s", dest="smartinit", action="store_true", help="smart initialize of parameters", default=False)
    parser.add_option("--stopwords", dest="stopwords", help="exclude stop words", action="store_true", default=False)
    parser.add_option("--seed", dest="seed", type="int", help="random seed")
    parser.add_option("--df", dest="df", type="int", help="threshold of document freaquency to cut words", default=0)
    (options, args) = parser.parse_args()
    # if not (options.filename or options.corpus): parser.error("need corpus filename(-f) or corpus range(-c)")

    # コーパスの読み込み
    if options.filename:
        corpus = vocabulary.load_file(options.filename)
        categories = []
    else:
        corpus, categories = vocabulary.load_corpus()
    # 乱数のシード設定
    if options.seed != None:
        numpy.random.seed(options.seed)
    # コーパス中の文書をbag of wordsに変形
    voca = vocabulary.Vocabulary(options.stopwords)
    docs = [voca.doc_to_ids(doc) for doc in corpus]
    # 低頻度の語彙をカット
    if options.df > 0: docs = voca.cut_low_freq(docs, options.df)
    # LDAの初期設定
    lda = LDA(options.K, options.alpha, options.beta, docs, voca.size(), options.smartinit)
    print "corpus=%d, words=%d, K=%d, a=%f, b=%f" % (len(corpus), len(voca.vocas), options.K, options.alpha, options.beta)

    # 推論(指定回数分回したら文書-トピック分布を返す)
    thetas = lda_learning(lda, options.iteration, voca)
    address = './c10_t' + str(options.K) + '_a' + str(options.alpha) + '_b' + str(options.beta) + '_i' + str(options.iteration)
    # 保存用のファイルオープン
    # dic = shelve.open(address)
    # dic['thetas'] = thetas
    # dic['categories'] = numpy.array(categories)
    # dic.close()
    print "end!"
    print thetas[100]

def test():
    import vocabulary
    corpus, categories = vocabulary.load_corpus()
    print categories[20]
    for word in corpus[20]:
        print word
    print "success!!"

if __name__ == "__main__":
    # test()
    main()
