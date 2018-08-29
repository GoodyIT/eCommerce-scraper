# from subprocess import check_output
# check_output("scrapy crawl mango", shell=True)

import random

f = open('data/code_list.txt', 'w+')

for x in range(0, 100000):
    content = str(random.randint(100000000000,999999999999)) + '\n'
    f.write(content)

f.close()