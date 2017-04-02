with open(r"..\data\weibo.csv", 'r', encoding="utf-8") as in_f:
    with open(r"..\data\serach_result.csv", 'w', encoding="utf-8") as out_f:
        out_f.write(in_f.readline())
        line = in_f.readline()
        count = 0
        while line:
            tokens = line.split(',')
            if len(tokens) == 6:
                content = tokens[0] + tokens[4]
                if content.find("官员") != -1 or content.find("政府") != -1:
                    out_f.write(line)
                    count += 1
            line = in_f.readline()
            if count % 100 == 0:
                print("%d result found" % count)
print("%d result in total" % count)
