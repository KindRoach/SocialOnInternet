import pandas as pd

import weibo_reader.weiboReader_LineByLine as wr

pd.set_option('display.unicode.east_asian_width', True)
pd.options.display.width = 300
weibos = wr.Weibo_Reader_Line_by_Line(r"..\data\weibo.csv")
keywords = ["帝吧", "赵薇事件", "南海", "中国一点都不能少", "萨德", "颜色革命", "公知", "意识形态要闻", "毛泽东", "共青团", "小粉红"]
table = pd.DataFrame(data=0, index=keywords, columns=keywords)

pairs = list()
for i in range(0, 11):
    for j in range(i + 1, 11):
        pairs.append((keywords[i], keywords[j]))

count = 0
keywords_frequency = dict()
for content in weibos.contents():
    for key in keywords:
        if content.find(key) != -1:
            keywords_frequency[key] = keywords_frequency.get(key, 0) + 1
    for pair in pairs:
        if content.find(pair[0]) != -1 and content.find(pair[1]) != -1:
            table[pair[0]][pair[1]] += 1
    count += 1

for i in range(0, 11):
    for j in range(i, 11):
        table[keywords[j]][keywords[i]] = -1
print(table)

print(keywords_frequency)
for k, v in keywords_frequency.items():
    keywords_frequency[k] = v / count * 1000
print(keywords_frequency)
