from nltk.corpus import reuters
count = 0
count2 = 0
dic = {}
category_dic = {'crude':0, 'trade':1, 'money-fx':2, 'interest':3, 'money-supply':4, 'ship':5, 'sugar':6, 'coffee':7, 'gold':8, 'gnp':9}
for fileid in reuters.fileids():
	if len(reuters.categories(fileid)) != 1:
		# print(reuters.categories(fileid))
		count += 1
	else:
		for category in reuters.categories(fileid):
			if category in category_dic:
				count2 += 1
			dic.setdefault(category,0)
			dic[category] += 1

one_topic_documents = len(reuters.fileids()) - count
print(len(reuters.fileids()))
print(count)
print(count2)
print(one_topic_documents)
# print(dic.sorted(key = lambda (x,y):-y))
print(sorted(dic.items(), key=lambda x: -x[1]))