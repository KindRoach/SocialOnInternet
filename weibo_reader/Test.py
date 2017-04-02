import csv

with open(r"../data/test.csv", 'w', encoding="utf-8", newline="") as in_f:
    headers = ["name", "age"]
    writter = csv.DictWriter(in_f, headers)
    writter.writeheader()
    writter.writerows([{"name": "zhang", "age": 20},
                       {"name": "sen", "age": 21}])
