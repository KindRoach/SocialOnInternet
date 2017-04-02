import operator

frequency = {}
with open(r"..\data\words.txt", 'r', encoding="utf-8") as in_f:
    line = in_f.readline()
    while line:
        tokens = line.split(' ')
        while "的" in set(tokens):
            tokens.remove("的")
        for i in range(0, len(tokens) - 1):
            word = tokens[i] + ' ' + tokens[i + 1]
            frequency[word] = frequency.get(word, 0) + 1
        line = in_f.readline()
frequency = sorted(frequency.items(), key=operator.itemgetter(1))
for pair in frequency[-1000:]:
    print(pair)
