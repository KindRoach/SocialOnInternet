import re
from operator import itemgetter

import jieba
import zhon.hanzi as chinese
import weibo_reader.weiboReader_LineByLine as wr

re_chinese = re.compile('[%s]' % chinese.characters)


def jieba_tokenizer(doc):
    tokens = jieba.cut(doc)
    return [word for word in tokens
            if len(word) > 1
            and re_chinese.match(word)]


weiboes = wr.Weibo_Reader_Line_by_Line(r"../data/weibo.csv")
texts = (item.content for item in weiboes.weibo_items())
jieba_results = (jieba_tokenizer(text) for text in texts)
dic = dict()
for words in jieba_results:
    for word in words:
        dic[word] = dic.get(word, 0) + 1
sorted_dic = sorted(dic.items(), key=itemgetter(1), reverse=True)
with open(r"..\data\word_frequency.txt", "w", encoding="utf-8") as out_f:
    for k, v in sorted_dic:
        out_f.write("%s:%d\n" % (k, v))
