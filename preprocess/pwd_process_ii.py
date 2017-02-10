# -*- coding:utf-8 -*-

import codecs
import re
import pickle

local_file = r'D:\data\leak_final_20161219\correlation_final_data.txt'
output_file = codecs.open(r'D:\data\leak_final_20161219\correlation_dataset.txt', 'w', 'utf-8')

# [email_prefix, pwd, name, '\01'.join(pinyin), id, gender, username, mobile, src]
correlation_dataset = list()
line_cnt = 0
batch_size = 1000000
filter_list = [u'\ufffd', u'\u01d5', u'\xe5']
username_reg = r'^[a-zA-Z0-9_\- ]*$'
email_reg = r'^[a-zA-Z0-9_\-.]*$'
hanzi_reg = u'^[\u4e00-\u9fa5]*$'
pwd_reg = r'^[a-zA-Z0-9._@$%&*+!#)\-=\[\]",`~:;<(>^{}\'/\\?\| ]+$'
min_len = 6
max_len = 20
bad_name_cnt = 0
for line in codecs.open(local_file, 'r', 'utf-8'):
    line_cnt += 1
    if line_cnt % batch_size == 0:
        print("%dM->%d" % (line_cnt/batch_size, bad_name_cnt))
    pieces = line.split('\t')
    email_prefix = pieces[0].strip()
    if not re.match(email_reg, email_prefix):
        email_prefix = ''
    pwd = pieces[1].strip()
    if len(pwd) > max_len or len(pwd) < min_len:
        continue
    name = pieces[2].strip()
    if not re.match(hanzi_reg, name):
        bad_name_cnt += 1
        continue
    pinyin = pieces[3]
    id = pieces[4].strip()
    birth = pieces[5].strip()
    gender = pieces[6].strip()
    username = pieces[7].strip()
    mobile = pieces[8].strip()
    src = pieces[9].strip()
    ok = True
    for sample in filter_list:
        if sample in pwd:
            ok = False
            break
    if not ok:
        continue
    if not re.match(pwd_reg, pwd):
        continue
    if not re.match(username_reg, username):
        username = ''
    cur_result = [email_prefix, name, pinyin, id, birth, gender, username, mobile, src, pwd.strip()]
    output_file.writelines('\t'.join(cur_result)+'\n')
output_file.flush()
output_file.close()
print(line_cnt)
print(bad_name_cnt)

