import operator
import os

import pandas as pd
import jieba as jb
import zhon.hanzi as chinese
import re

from wordcloud import wordcloud


def show_weibo_content(start, end):
    if end < start:
        print("调用show_weibo_content函数时")
        print("开始序号 必须小于或者等于 结束序号")
        return
    for i in range(start, end + 1):
        print(weiboes.index[i], weiboes["博文类型"][i], weiboes["博文发表时间"][i], end=' ')
        if weiboes["博文类型"][i] == "原创":
            print(weiboes["博文"][i])
        else:
            print(weiboes["转发博文内容"][i])


# 获取指定序号区间的所有微博内容
# 如果微博为转发，则返回转发内容
def get_weibo_content(weiboes, start, end):
    ans = []
    # 判断微博是原创还是转发
    for i in range(start, end):
        if weiboes["博文类型"][i] == "原创":
            ans.append(weiboes["博文"][i])
        else:  # 转发
            ans.append(weiboes["转发博文内容"][i])
    return ans


# 找出列表中所有的中文字符，支持list嵌套
# 返回一个不嵌套的list
def find_all_chinese(words):
    ans = []
    # 因为分词的结果形如[["国防部"，"部长"...],["年轻人","鲁迅"...]...]
    # 它是list中嵌套了list
    # 所以对于words中的每个元素，首先要判断是否是一个字符串
    # 如果是字符串，直接处理
    # 否则递归调用find_all_chinese()函数
    for item in words:
        # 如果是字符串
        if isinstance(item, str):
            # 判断字符串是否是中文字符
            if re.match('[%s]' % chinese.characters, item):
                ans.append(item)
        # 如果是list
        elif isinstance(item, list):
            for word in find_all_chinese(item):
                ans.append(word)
    return ans


# 统计各词汇出现的频率
# 返回dict[string:float]
# 传入的list不支持嵌套！
def get_shown_times(words):
    ans = {}
    # 遍历words中的每个词
    for word in words:
        # 如果这个词在字典当中（即以前出现过）
        if word in ans:
            # 该词出现次数+1
            ans[word] += 1
        else:  # 不再字典中（即以前没有出现过）
            # 将该词加入字典，并且把出现次数记为1
            ans[word] = 1
    # 通过各词出现的次数计算其出现频率（出现次数/总数）
    for key, value in ans.items():
        ans[key] /= len(words)
    return ans


# 制作词云，传入的list不支持嵌套！
# 参数words是一个记录了各词汇出现频率的字典
# path是要保存图像的路径（""即直接保存在py文件目录下）
# name是要保存的图像名称
def get_word_cloud_image(shown_times, path, name):
    # font_path即字体文件的路径，这里仅适用于windows，使用的是微软雅黑
    # width和height即生成图像的大小，可以设置更小的值以减少计算量
    wcloud = wordcloud.WordCloud(font_path=r"C:\Windows\Fonts\msyh.ttc", width=5000, height=5000)
    print("生成图像...")
    wcloud.generate_from_frequencies(shown_times)
    # wcloud.to_image()函数只是生成了图像
    # 还需要用另一个变量wc_image接住返回值
    wc_image = wcloud.to_image()
    # 调用wc_image的save函数才能真正保存图像
    wc_image.save(os.path.join(path, name + ".PNG"), "PNG")
    print("图像已保存：%s" % os.path.join(path, name + ".PNG"))


print("读取数据...")
weiboes = pd.read_csv("weibo.csv")
# start=0, end=len(weiboes) - 1 即为整个weiboes
# 可以指定更小的区间，以减少计算量
weibo_content = get_weibo_content(weiboes, 0, len(weiboes) - 1)
# 分词计算量较大，请耐心等待
print("分词中...")
words = [jb.lcut(item) for item in weibo_content]
print("过滤非中文字符...")
chinese_words = find_all_chinese(words)
# 生成图像的计算量也很大，请耐心等待
print("统计词频...")
shown_times = get_shown_times(chinese_words)
# get_word_cloud_image(shown_times, "", "wordcloud")
sorted_x = sorted(shown_times.items(), key=operator.itemgetter(1))
for k, v in sorted_x[-1000:]:
    print(k, v)
