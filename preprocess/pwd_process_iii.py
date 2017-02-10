# -*- coding:utf-8 -*-
import codecs
import random
import os

local_file = r'D:\data\leak_final_20161219\correlation_dataset.txt'

# email_prefix, name, pinyin, id, birth, gender, username, mobile, src, pwd
ratios = [0.8, 0.9]

version = 'pipw_1.0'
paths = [r'D:\data\leak_final_20161219\pipw\train\all_pi-pw.pi.tok',
         r'D:\data\leak_final_20161219\pipw\train\all_pi-pw.pw.tok',
         r'D:\data\leak_final_20161219\pipw\dev\all_pi-pw.pi.tok',
         r'D:\data\leak_final_20161219\pipw\dev\all_pi-pw.pw.tok',
         r'D:\data\leak_final_20161219\pipw\test\all_pi-pw.pi.tok',
         r'D:\data\leak_final_20161219\pipw\test\all_pi-pw.pw.tok']

dirs = [r'D:\data\leak_final_20161219\pipw\train',
        r'D:\data\leak_final_20161219\pipw\dev',
        r'D:\data\leak_final_20161219\pipw\test']

paths = [path.replace('pipw', version) for path in paths]
dirs = [dir.replace('pipw', version) for dir in dirs]
[os.makedirs(dir) for dir in dirs if not os.path.exists(dir)]

files = [codecs.open(path, 'w', encoding='utf-8') for path in paths]
max_len = 0
max_len_trg = 0
line_cnt = 0
batch_size = 1000000
for line in codecs.open(local_file, 'r', 'utf-8'):
    line_cnt += 1
    if line_cnt % batch_size == 0:
        print("%dM" % int(line_cnt/batch_size))
    pieces = line.split('\t')
    email_prefix = pieces[0].strip()
    pinyin = ' '.join(pieces[2].strip().split('\01'))
    id = pieces[3]
    birth = pieces[4]
    username = pieces[6]
    mobile = pieces[7]
    pwd = pieces[9].strip()
    # version max_len max_len_trg
    # pipw_1.0 94 20
    # dict size
    # 3166 3234 69 97
    cur_feat = ' '.join([pinyin, birth, username, email_prefix])

    rng = random.random()
    if len(cur_feat) > max_len:
        max_len = len(cur_feat)
    if len(pwd) > max_len_trg:
        max_len_trg = len(pwd)
    if rng <= ratios[0]:
        files[0].writelines(cur_feat + '\n')
        files[1].writelines(pwd + '\n')
    elif rng < ratios[1]:
        files[2].writelines(cur_feat + '\n')
        files[3].writelines(pwd + '\n')
    else:
        files[4].writelines(cur_feat + '\n')
        files[5].writelines(pwd + '\n')
[handler.flush() for handler in files]
[handler.close() for handler in files]
print("Total line count:%d" % line_cnt)
print("Max feature length:%d" % max_len)
print("Max password length:%d" % max_len_trg)
