import os
import re
import csv

import jieba
import multiprocessing
import zhon.hanzi as chinese
from gensim import corpora
from gensim import models
from gensim.models import CoherenceModel


def get_stop_words():
    words = set()
    with open(r"../data/my_stopwords.txt", 'r', encoding="utf-8") as in_f:
        for line in in_f:
            words.add(line[0:-1])
    return words


def jieba_tokenizer(doc):
    tokens = jieba.cut(doc)
    return [word for word in tokens
            if len(word) > 1
            and word not in stop_words
            and re_chinese.match(word)]


def get_dic_cor():
    if not os.path.exists(dict_path):
        reader = csv.reader(open(csv_path, encoding="UTF8"), delimiter=",")
        texts = [jieba_tokenizer(line[0] + line[4]) for line in reader]
        dictionary = corpora.Dictionary(texts)
        dictionary.save(dict_path)
        corpus = [dictionary.doc2bow(text) for text in texts]
        corpora.MmCorpus.serialize(mm_path, corpus)


def run_model(N, print_topic, dictionary, corpus, lines):
    topic_folder_path = "topics" + str(N)
    lda_path = topic_folder_path + "/" + "model.lda." + str(N)

    if not os.path.exists(topic_folder_path):
        os.makedirs(topic_folder_path)

    if os.path.exists(lda_path):
        lda = models.LdaModel.load(lda_path)
    else:
        lda = models.LdaModel(corpus, id2word=dictionary, num_topics=N)
        lda.save(lda_path)

    with open(topic_folder_path + "/topics.txt", "w", encoding="utf-8") as f:
        topics = lda.show_topics(num_topics=N, num_words=10)
        for topic in topics:
            f.write(topic.__str__() + "\n")

    if print_topic:

        topics = [list() for i in range(N)]
        count = 0
        for x in corpus:
            vec = lda[x]
            vec = sorted(vec, key=lambda x: x[1], reverse=True)
            i = vec[0][0]
            topics[i].append((vec[0][1], lines[count]))
            count += 1

        for i in range(N):
            topics[i] = sorted(topics[i], key=lambda x: x[0], reverse=True)
            with open(topic_folder_path + "/topic" + str(i) + ".csv", "w", encoding="utf-8") as f:
                for x in topics[i]:
                    f.write(x[1])

    cm = CoherenceModel(model=lda, corpus=corpus, coherence='u_mass')
    print(N, '\t', cm.get_coherence())


if __name__ == '__main__':
    stop_words = get_stop_words()
    re_chinese = re.compile('[%s]' % chinese.characters)

    work_path = r"../data/topic_model/china"
    csv_path = "model.csv"
    dict_path = "model.dict"
    mm_path = "model.mm"
    os.chdir(work_path)

    get_dic_cor()

    dictionary = corpora.Dictionary.load(dict_path)
    corpus = corpora.MmCorpus(mm_path)

    lines = list()
    with open(csv_path, "r", encoding="UTF8") as reader:
        lines = list(reader.readlines())

    p = multiprocessing.Pool()
    for i in range(5, 51):
        p.apply_async(run_model, args=(i, False, dictionary, corpus, lines))
    p.close()
    p.join()
    print("ALL DONE!")
