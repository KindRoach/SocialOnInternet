import os

import jieba
import re
import zhon.hanzi as chinese
from wordcloud import wordcloud


class Weibo_item(object):
    def __init__(self, writter, writter_id, datetime, content, forwarder, forwarder_id):
        self.writter = writter
        self.writter_id = writter_id
        self.datetime = datetime
        self.content = content
        self.forwarder = forwarder
        self.forwarder_id = forwarder_id


class Weibo_Reader_Line_by_Line(object):
    def __init__(self, path):
        self.read_line = -2
        self.f = open(path, 'r', encoding="utf-8")

    def __del__(self):
        self.f.close()

    # 初始化文件指针的位置
    def initail(self):
        self.f.seek(0)
        # 跳过"博文,博文发表时间,博文类型,微博博主名,转发博文内容,转发博文的博主名"标题这一行
        self.f.readline()
        self.read_line = -1

    # 打印指定序号区间的微博
    # 逐行读入csv文件
    # 如果要查看的微博还未读取过，则从文件的当前位置继续读取
    # 否则，调用seek函数将文件指针重新指向文件开始处
    def print_weibo_content(self, start, end):
        if start <= self.read_line:
            self.initail()
        while self.read_line < end:
            self.read_line += 1
            line = self.f.readline()
            if not line:
                return
            tokens = line.split(',')
            if len(tokens) != 6:
                continue
            if self.read_line >= start:
                print(self.read_line, tokens[2], tokens[1], end=' ')
                if tokens[2] == "原创":
                    print(tokens[0])
                else:
                    print(tokens[4])

    # 逐行读取csv文件
    # 返回迭代器
    def lines(self):
        self.initail()
        line = "fake line"
        while line:
            line = self.f.readline()
            self.read_line += 1
            yield line

    # 返回微博内容的迭代器
    def contents(self):
        for line in self.lines():
            tokens = line.split(',')
            if len(tokens) != 6:
                continue
            if tokens[2] == "原创":
                yield tokens[0]
            else:
                yield tokens[0] + " // " + tokens[4]

    def get_word_frequency(self):
        ans = {}
        print("计算词频...")
        for line in self.lines():
            tokens = line.split(',')
            if tokens[2] == "原创":
                content = tokens[0]
            else:
                content = tokens[4]
            words = jieba.lcut(content)
            for word in words:
                if re.match('[%s]' % chinese.characters, word):
                    if word in ans:
                        ans[word] += 1
                    else:
                        ans[word] = 1
        total_count = 0
        for key, value in ans.items():
            total_count += ans[key]
        for key, value in ans.items():
            ans[key] /= total_count
        return ans

    def weibo_items(self):
        user_count = 0
        user = dict()
        for line in self.lines():
            tokens = line.split(',')
            if len(tokens) != 6:
                continue
            writter = tokens[3]
            if writter in user:
                writter_id = user[writter]
            else:
                user_count += 1
                writter_id = user_count
                user[writter] = user_count
            datetime = tokens[1]
            content = tokens[0]
            if tokens[2] == "原创":
                forwarder = "/"
                forwarder_id = -1
            else:
                content += tokens[4]
                forwarder = tokens[5][0:-1]
                if forwarder in user:
                    forwarder_id = user[forwarder]
                else:
                    user_count += 1
                    forwarder_id = user_count
                    user[forwarder] = user_count
            yield Weibo_item(writter, writter_id, datetime, content, forwarder, forwarder_id)


# 制作词云，传入的list不支持嵌套！
# 参数words是一个记录了各词汇出现频率的字典
# path是要保存图像的路径（""即直接保存在py文件目录下）
# name是要保存的图像名称
def get_word_cloud_image(word_frequency, path, name):
    # font_path即字体文件的路径，这里仅适用于windows，使用的是微软雅黑
    # width和height即生成图像的大小，可以设置更小的值以减少计算量
    wcloud = wordcloud.WordCloud(font_path=r"C:\Windows\Fonts\msyh.ttc", width=500, height=500)
    print("生成图像...")
    wcloud.generate_from_frequencies(word_frequency)
    # wcloud.to_image()函数只是生成了图像
    # 还需要用另一个变量wc_image接住返回值
    wc_image = wcloud.to_image()
    # 调用wc_image的save函数才能真正保存图像
    wc_image.save(os.path.join(path, name + ".PNG"), "PNG")
    print("图像已保存：%s" % os.path.join(path, name + ".PNG"))


if __name__ == "__main__":
    # 博文,博文发表时间,博文类型,微博博主名,转发博文内容,转发博文的博主名
    reader = Weibo_Reader_Line_by_Line("..\data\weibo.csv")
    # reader.print_weibo_content(0, 100)
    # reader.print_weibo_content(100, 200)
    # word_frequency = reader.get_word_frequency()
    # get_word_cloud_image(word_frequency, "", "5")
    for content in reader.contents():
        print(content)
