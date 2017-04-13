import re

s = "中国政府警告"
ss = "中国政府官员"
sss = "没有"

re_gov = re.compile("政府|官员")
if re_gov.search(s):
    print(s)
if re_gov.search(ss):
    print(ss)
if re_gov.search(sss):
    print(sss)
