import re

# my_filter = re.compile(r"[帝吧|赵薇|南海|中国|萨德|颜色革命|公知|意识形态|毛泽东|共青团|小粉红|爱国]")
my_filter = re.compile(r"中国")

with open(r"..\data\weibo.csv", "r", encoding="utf-8") as in_f:
    with open(r"..\data\china.csv", "w", encoding="utf-8") as out_f:
        for line in in_f:
            if my_filter.search(line):
                out_f.write(line)
