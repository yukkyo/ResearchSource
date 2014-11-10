#!/usr/bin/env python
# -*- coding: utf-8 -*-

# lda.pyで求めた文書トピック分布を用いてsvm-multi classiferを実装，およびmatplotlibでの図示

from sklearn.datasets import load_digits
from sklearn.cross_validation import train_test_split
from sklearn.svm import LinearSVC

# データとラベルを受け取ってsvmを実行
def svm(data, label):
	# トレーニングデータとテストデータに分割
	data_train, data_test, label_train, label_test = train_test_split(data, label)
	# 分類器にパラメータを与える
	estimator = LinearSVC(C=1.0)
	# トレーニングデータで学習する
	estimator.fit(data_train, label_train)
	# テストデータの予測をする
	label_predict = estimator.predict(data_test)

	return label_predict, label_test

def main():
	# shelveでオープン

	# svmを実行

	# 図示


def test():
	# 不安だったらここで確認

if __name__ == "__main__":
    test()
    # main()