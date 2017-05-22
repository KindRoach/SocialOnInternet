import pandas as pd
import weibo_reader.weiboReader_LineByLine as wr

pd.set_option('display.unicode.east_asian_width', True)
pd.options.display.width = 300
weibos = wr.Weibo_Reader_Line_by_Line(r"..\data\weibo.csv")

users = set()

items = list(weibos.weibo_items())
for item in items:
    users.add(item.writter)

user2id = dict()
i = 0
for user in users:
    user2id[user] = i
    i += 1

user_list = list(users)
table = pd.DataFrame(data=0, columns=range(len(users)), index=range(len(users)))

for item in items:
    if item.forwarder in users:
        table[user2id[item.writter]][user2id[item.forwarder]] += 1

with open(r"../data/forward_map.txt", 'w', encoding="utf-8") as out_f:
    for i in range(len(users)):
        for j in range(len(users)-1):
            out_f.write(str(table[i][j])+' ')
        out_f.write(str(table[i][len(users)-1])+'\n')
