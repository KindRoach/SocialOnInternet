import os
import re
import csv
from itertools import tee

import jieba
import zhon.hanzi as chinese
from gensim import corpora
from gensim import models


def get_stop_words():
    with open(r"../data/chinese_stopwords.txt", 'r', encoding="utf-8") as in_f:
        words = set(in_f.readlines())
    return words


def jieba_tokenizer(doc):
    tokens = jieba.cut(doc)
    return [word for word in tokens
            if len(word) > 1
            and word not in stop_words
            and re_chinese.match(word)]


stop_words = get_stop_words()
re_chinese = re.compile('[%s]' % chinese.characters)
re_gov = re.compile("公知")

# 保存dictionary和corpus，以供随后使用
dict_path = r"../data/weibo.dict"
mm_path = r"../data/weibo.mm"
if os.path.exists(dict_path):
    dictionary = corpora.Dictionary.load(dict_path)
    corpus = corpora.MmCorpus(mm_path)
else:
    reader = csv.reader(open(r"../data/weibo.csv", encoding="UTF8"), delimiter=",")
    texts = (jieba_tokenizer(line[0] + line[4]) for line in reader if re_gov.search(line[0]) or re_gov.search(line[4]))
    texts, texts_backup = tee(texts)
    dictionary = corpora.Dictionary(texts)
    dictionary.save(r"../data/weibo.dict")
    corpus = [dictionary.doc2bow(text) for text in texts_backup]
    corpora.MmCorpus.serialize(mm_path, corpus)

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=10)
topics = lsi.show_topics()
for topic in topics:
    print(topic[1])
