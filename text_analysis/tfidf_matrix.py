import re

import jieba
import zhon.hanzi as chinese
from scipy import linalg as LA
from sklearn.feature_extraction.text import CountVectorizer

import text_analysis.chinese_stopwords as cs
import weibo_reader.weiboReader_LineByLine as wr

stop_words = cs.get_stop_words()
re_chinese = re.compile('[%s]' % chinese.characters)


def jieba_tokenizer(doc):
    tokens = jieba.cut(doc)
    return [word for word in tokens
            if len(word) > 1
            and word not in stop_words
            and re_chinese.match(word)]


weiboes = wr.Weibo_Reader_Line_by_Line(r"../data/weibo.csv")
texts = [item.content for item in weiboes.weibo_items()]
count_vect = CountVectorizer(tokenizer=jieba_tokenizer)
dtm = count_vect.fit_transform(texts)
# print(count_vect.get_feature_names())
# print(dtm.shape)
# print(dtm)
# tfidf_transformer = TfidfTransformer().fit(dtm)
# dtm_tfidf = tfidf_transformer.transform(dtm)
# print(dtm_tfidf.shape)
# print(dtm_tfidf)
u, s, vt = LA.svd(dtm)
print(u)
print(s)
print(vt)
