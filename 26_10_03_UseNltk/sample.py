# ロイターコーパスにおいて複数のカテゴリが割り当てられてる記事の個数をカウントする
from nltk.corpus import reuters
count = 0
for fileid in reuters.fileids():
	if len(reuters.categories(fileid)) != 1:
		# print(reuters.categories(fileid))
		count += 1
one_topic_documents = len(reuters.fileids()) - count
print(len(reuters.fileids()))
print(count)
print(one_topic_documents)