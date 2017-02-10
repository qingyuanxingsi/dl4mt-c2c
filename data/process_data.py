# -*- coding:utf-8 -*-

import codecs
from pypinyin import lazy_pinyin
import pickle
import re
from datetime import datetime

data_list = list()
min_len = 6
max_len = 20
data_12306_file = r'D:\data\leak_final_20161219\12306_leak.txt'
data_extra_file = r'D:\data\leak_final_20161219\correlation_data.txt'
output_file = codecs.open(r'D:\data\leak_final_20161219\correlation_final_data.txt', 'w', 'utf-8')
username_reg = '^\w*$'
name_reg = '[a-zA-Z]+'

muls = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
mod_dict = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']


def convert_id(id):
    """
    convert id
    :param id:
    :return:
    """
    try:
        id_trans = id[0:6] + '19' + id[6:]
        id_check = [int(ch) for ch in id_trans]
        sum = 0
        for idx in range(0, len(id)):
            sum += id_check[idx] * muls[idx]
        verify_code = mod_dict[sum % 11]
        return id_trans + verify_code, True
    except Exception as ex:
        return '', False


print('processing 12306...')
final_cnt = 0
for line in codecs.open(data_12306_file, 'r', 'gbk'):
    pieces = line.strip().split('----')
    email = pieces[0]
    pwd = pieces[1]
    if len(pwd) > max_len or len(pwd) < min_len:
        continue
    name = pieces[2]
    id = pieces[3]
    username = pieces[4]
    mobile = pieces[5]
    email_prefix = email[0:email.find('@')]
    pinyin = lazy_pinyin(name)
    len_id = len(id)
    if len_id not in [15, 18]:
        continue
    if len_id == 15:
        id, ok = convert_id(id)
        if not ok:
            continue
    birth = id[6:14]
    src = '12306'
    gender = 'UNK'
    if len(id) != 0:
        gender_int = int(id[16])
        if gender_int % 2 == 0:
            gender = 'F'
        else:
            gender = 'M'
    # email pwd name pinyin id username mobile src
    cur_result = [email_prefix, pwd, name, '\01'.join(pinyin), id, birth, gender, username, mobile, src]
    output_file.writelines('\t'.join(cur_result)+'\n')
    final_cnt += 1
print('done...')

print('Processing extra data...')
extra_data = codecs.open(data_extra_file, 'r', 'utf-8')
line = extra_data.readline()
batch_size = 1000000
line_cnt = 0
bad_name = 0
bad_id_cnt = 0
bad_pwd_len_cnt = 0
for line in extra_data:
    line_cnt += 1
    if line_cnt % batch_size == 0:
        cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("%s->%dM->%d" % (cur_time, line_cnt/batch_size, bad_pwd_len_cnt))
    pieces = line.split('\t')
    if len(pieces) != 11:
        continue
    username = pieces[0]
    pwd = pieces[1]
    email = pieces[3]
    src = pieces[4].strip()
    name = pieces[5]
    if re.match(name_reg, name):
        bad_name += 1
        continue
    id = pieces[7]
    gender = pieces[8]
    birth = pieces[9]
    mobile = pieces[10].strip()
    if len(pwd) > max_len or len(pwd) < min_len:
        bad_pwd_len_cnt += 1
        continue
    email_prefix = email[0:email.find('@')]
    pinyin = lazy_pinyin(name)
    len_id = len(id)
    if len_id not in [0, 15, 18]:
        continue
    if len_id == 15:
        id, ok = convert_id(id)
        if not ok:
            continue
    gender = 'UNK'
    if len(id) != 0:
        try:
            gender_int = int(id[16])
            if gender_int % 2 == 0:
                gender = 'F'
            else:
                gender = 'M'
        except Exception as ex:
            bad_id_cnt += 1
            continue
        birth = id[6:14]
    if len(mobile) not in [0, 11]:
        mobile = ''
    cur_result = [email_prefix, pwd, name, '\01'.join(pinyin), id, birth, gender, username, mobile, src]
    output_file.writelines('\t'.join(cur_result)+'\n')
    final_cnt += 1
output_file.flush()
output_file.close()
print('done...')

print(final_cnt)
print("Bad name count:%d" % bad_name)
print("Bad id count:%d" % bad_id_cnt)
print("Bad password length count:%d" % bad_pwd_len_cnt)
# print('dumping dataset...')
# data_desc = ['email_prefix', 'pwd', 'name', 'pinyin', 'id', 'gender', 'username', 'mobile', 'src']
# pickle.dump([data_desc, data_list], open(output_file, 'wb'))
# print('done...')

