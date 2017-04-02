import pandas as pd
import weibo_reader.weiboReader_LineByLine as wr

pd.set_option('display.unicode.east_asian_width', True)
pd.options.display.width = 300
weibos = wr.Weibo_Reader_Line_by_Line(r"..\data\weibo.csv")
keywords = ["帝吧", "赵薇事件", "南海", "中国一点都不能少", "萨德", "颜色革命", "公知", "意识形态要闻", "毛泽东", "共青团", "小粉红"]
users = set()
items = list(weibos.weibo_items())
for item in items:
    users.add(item.writter)
user_list = list(users)
table = pd.DataFrame(data=0, columns=user_list, index=user_list)
for item in items:
    for user in users:
        if item.content.find(user) != -1 or item.forwarder == user:
            topic_found = False
            for key in keywords:
                if item.content.find(key) != -1:
                    topic_found = True
            if topic_found:
                table[item.writter][user] += 1
for userA in user_list:
    for userB in user_list:
        if table[userA][userB] > 0 and table[userB][userA] > 0 and userA != userB:
            print("%s:%s:%d" % (userA, userB, max(table[userA][userB], table[userB][userA])))
# print(table)
