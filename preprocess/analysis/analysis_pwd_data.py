# -*- coding:utf-8 -*-

import codecs

local_file = r'D:\data\leak_final\correlation_dataset.txt'

src_dict = dict()
"""
weibo	181317
duduniu	2686852
17173	4122360
tianya	730183
kaixin	1467298
ys168	59192
gmail	914
yahoo	224
zhenai	449304
renren	181329
12306	131112
qiannao	180496
126	132585
7k7k	229579
csdn	69695
vip_qq	311
163	5519459
"""
# email_prefix, name, pinyin, id, birth, gender, username, mobile, src, pwd
batch_size = 1000000
cur_cnt = 0
for line in codecs.open(local_file):
    cur_cnt += 1
    if cur_cnt % batch_size == 0:
        print("%dM" % int(cur_cnt/batch_size))
    pieces = line.rstrip().split('\t')
    email_prefix = pieces[0]
    name = pieces[1]
    pinyin = pieces[2]
    id = pieces[3]
    birth = pieces[4]
    gender = pieces[5]
    username = pieces[6]
    mobile = pieces[7]
    src = pieces[8]
    pwd = pieces[9]
    if src not in src_dict:
        src_dict[src] = 1
    else:
        src_dict[src] += 1

for key, value in src_dict.items():
    print(key+"\t"+str(value))

print(cur_cnt)