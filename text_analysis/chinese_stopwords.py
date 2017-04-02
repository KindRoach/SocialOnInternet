def get_stop_words():
    with open(r"../data/chinese_stopwords.txt", 'r', encoding="utf-8") as in_f:
        words = set(in_f.readlines())
    return words


def test():
    words = get_stop_words()
    print(words)
    print(len(words))


if __name__ == "__main__":
    test()
