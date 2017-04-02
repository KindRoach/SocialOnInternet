import weibo_reader.weiboReader_LineByLine as wr

weibos = wr.Weibo_Reader_Line_by_Line(r"..\data\weibo.csv")
writter = "NUxpTjVyS0o2YnVZNTVxRTVhU241YVNhNXBXdw=="
forwarder = "NmJLTjZMK3E1WVdM"
for item in weibos.weibo_items():
    if (writter == item.writter) and (forwarder == item.forwarder):
        print(item.content)
