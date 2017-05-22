import weibo_reader.weiboReader_LineByLine as wr

weibos = wr.Weibo_Reader_Line_by_Line(r"..\data\weibo.csv")
users = set([x.writter for x in weibos.weibo_items()])
user2id = dict()
i = 0
for user in users:
    user2id[user] = i
    i += 1
print(user2id)
with open(r"../data/user2id.csv", 'w', encoding="utf-8") as out_f:
    for k, v in user2id.items():
        out_f.write("%s,%d\n" % (k, v))
