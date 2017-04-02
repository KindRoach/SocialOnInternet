import jieba
import re
import zhon.hanzi as chinese

import weibo_reader.weiboReader_LineByLine as wr

weibos = wr.Weibo_Reader_Line_by_Line(r"..\data\weibo.csv")
re_chinese = re.compile('[%s]' % chinese.characters)
content_set = set(weibos.contents())
with open(r"..\data\word_breaker_result.txt", "w", encoding="utf-8") as out_f:
    count = 0
    for content in content_set:
        ans = []
        words = jieba.cut(content)
        for word in words:
            if re_chinese.match(word):
                ans.append(word)
        for i in range(0, len(ans)):
            if i < len(ans) - 1:
                out_f.write(ans[i] + ' ')
            else:
                out_f.write(ans[i] + "\n")
        count += 1
        if count % 1000 == 0:
            print("%d / %d lines finished" % (count, len(content_set)))
