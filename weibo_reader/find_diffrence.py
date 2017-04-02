import pandas

# 使用read_csv()从csv文件中读取数据
weiboes = pandas.read_csv(r"../data/weibo.csv", sep=',')
weibo = set(weiboes["博文"].values)
in_f = open("../data/weibo.csv", 'r', encoding="utf8")
out_f = open("../data/difference.csv", 'w', encoding="utf8")

# 直接使用readlines()从csv文件中读取数据
lines = in_f.readlines()
print("read_csv函数忽略了%d行" % (len(lines)-len(weiboes)))
for line in lines:
    if len(line.split(',')) > 6:
        out_f.write(line)
in_f.close()
out_f.close()
