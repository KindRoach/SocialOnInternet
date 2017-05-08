import re

for i in range(20):
    for x in re.findall('"(.*?)"',input()):
        print(x,end='\t')
    print()
