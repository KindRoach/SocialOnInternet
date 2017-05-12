import csv

from gensim import models, corpora

lda_path = r"../data/lda10/china.lda.10"
csv_path = r"../data/china.csv"
mm_path = r"../data/model.mm"

lda = models.LdaModel.load(lda_path)

dict_list = [dict() for i in range(10)]
count_in_month = dict()
# dict_list = [0 for i in range(10)]

corpus = corpora.MmCorpus(mm_path)

reader = csv.reader(open(csv_path, encoding="UTF8"), delimiter=",")
count = 0
for x in corpus:
    # 2016-01-02-18-11
    date = next(reader)[1]
    if len(date) != 16:
        continue
    count += 1
    month = int(date[5: 7])
    count_in_month[month] = count_in_month.get(month, 0) + 1
    vec = lda[x]
    for item in vec:
        dict_list[item[0]][month] = item[1] + dict_list[item[0]].get(month, 0)
        # dict_list[item[0]] += item[1]

for month in range(1, 10):
    print("month:", month, end='\t')
    for i in range(10):
        print(dict_list[i][month] / count_in_month[month], end='\t')
    print()
print("total:", end='\t')
for i in range(10):
    top_sum = 0
    for month in range(1, 10):
        top_sum += dict_list[i][month]
    print(top_sum / count, end='\t')
