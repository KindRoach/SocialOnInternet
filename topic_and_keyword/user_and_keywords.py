import pandas as pd
import weibo_reader.weiboReader_LineByLine as wr

pd.set_option('display.unicode.east_asian_width', True)
pd.options.display.width = 300
weibos = wr.Weibo_Reader_Line_by_Line(r"..\data\weibo.csv")
keywords = ["帝吧", "赵薇事件", "南海", "中国一点都不能少", "萨德", "颜色革命", "公知", "意识形态要闻", "毛泽东", "共青团", "小粉红"]
users = set()
items = list(weibos.weibo_items())

for item in items:
    users.add(item.writter_id)
    # users.add(item.forwarder_id)

table = pd.DataFrame(data=0, columns=keywords, index=users)
for item in items:
    for key in keywords:
        if item.content.find(key) != -1:
            table[key][item.writter_id] += 1

for user in users:
    print("%-7d" % user, end=' ')
    for key in keywords:
        if table[key][user] > 0:
            s = "%s:%d" % (key, table[key][user])
            print("%-10s" % s, end=' ')
    print()

total_user_by_key = dict()
for key in keywords:
    print("%-7s" % key, end=' ')
    for user in users:
        if table[key][user] > 0:
            s = "%d:%d" % (user, table[key][user])
            print("%-10s" % s, end=' ')
            total_user_by_key[key] = total_user_by_key.get(key, 0) + 1
    print()
print(total_user_by_key)
