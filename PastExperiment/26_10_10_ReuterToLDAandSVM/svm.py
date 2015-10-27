#!/usr/bin/env python
# -*- coding: utf-8 -*-

# lda.pyで求めた文書トピック分布を用いてsvm-multi classiferを実装，およびmatplotlibでの図示

from sklearn.datasets import load_digits
from sklearn.cross_validation import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score

# データとラベルを受け取ってsvmを実行
def svm(data, label, train_size):
	# トレーニングデータとテストデータに分割
	data_train, data_test, label_train, label_test = train_test_split(data, label, train_size=train_size)
	# 分類器にパラメータを与える
	estimator = LinearSVC(C=1.0)
	# トレーニングデータで学習する
	estimator.fit(data_train, label_train)
	# テストデータの予測をする
	label_predict = estimator.predict(data_test)

	return label_predict, label_test

# 図示用
def plot_graph(all_error, rates):
	import matplotlib.pylot as plt

	# 各aによってerror rateが変わるかを図示
	plt.plot(rates, all_error[0],'ro',label = "alpha=0.1")
	plt.plot(rates, all_error[1],'b',label = "alpha=1.0")
	plt.plot(rates, all_error[2],label = "alpha=3.0")
	plt.plot(rates, all_error[3],label = "alpha=10.0")

	plt.legend() # 凡例を表示
	plt.xticks(rates,("","0.02","0.05","0.1","0.2"))
	# plt.title("Graph Title")
	plt.xlabel("Training Size")
	plt.ylabel("Error Rate")
	plt.show()
	# トピック次元によって

def main():
	rates = [0.01, 0.02, 0.05, 0.1, 0.2]
	files = ["1",
	"2",
	"3"]
	all_error = []
	# 各データについてsvmを実施する
	for f in files:
		# shelveでオープン
		dic = shelve.open(f)
		data = dic['thetas']
		label = dic['categories']
		error_rates = []
		for r in rates:
			# svmを実行
			label_predict, label_test = svm(data, label, r)
			# Error Rateを求める
			error_rates.append(1.0 - accuracy_score(label_predict, label_test))
		all_error.append(error_rates)
		dic.close()

	# 図示
	result = shelve.open('result')
	result['all_error'] = all_error
	result.close()
	plot_graph(all_error, rates)



def make_graph():
	# 不安だったらここで確認
	result = shelve.open('result')
	all_error = result['all_error']
	result.close()

if __name__ == "__main__":
    # test()
    main()
    make_graph()