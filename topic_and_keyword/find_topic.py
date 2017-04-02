import operator
import re
import weibo_reader.weiboReader_LineByLine as wr

re_topic = re.compile(r"#([^@*#<>]{4,32})#")
weibos = wr.Weibo_Reader_Line_by_Line(r"..\data\weibo.csv")
count = 0
topics = {}
for content in weibos.contents():
    for topic in re_topic.findall(content):
        if topic in topics:
            topics[topic] += 1
        else:
            topics[topic] = 1
topics = sorted(topics.items(), key=operator.itemgetter(1))
for pair in topics:
    print(pair)
