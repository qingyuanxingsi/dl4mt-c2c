# -*- encoding:utf-8 -*-
import pickle
from pypinyin import lazy_pinyin
import random
import os
import codecs
import random

muls = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
mod_dict = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
data_aug = False
shuffle_cnt = 3


# 102 16
# 2136 2190 70 76 no-aug
# 2120 2200 71 79 aug
def convert_id(id):
    """
    convert id
    :param id:
    :return:
    """
    id = id[0:6] + '19' + id[6:]
    id_check = [int(ch) for ch in id]
    sum = 0
    for idx in range(0, len(id)):
        sum += id_check[idx] * muls[idx]
    verify_code = mod_dict[sum % 11]
    return id + verify_code


# email, pwd, name, id, username, mobile
local_file = r'D:\data\leak_final_20161219\12306_leak.pkl'
data_list = pickle.load(open(local_file, 'rb'))
print(len(data_list))

dataset = list()
for data in data_list:
    email = data[0]
    pwd = data[1]
    name = data[2]
    id = data[3]
    username = data[4]
    mobile = data[5]
    email_prefix = email[0:email.find('@')]
    pinyin = lazy_pinyin(name)
    len_id = len(id)
    if len_id not in [15, 18]:
        continue
    if len_id == 15:
        id = convert_id(id)
    birth = id[6:14]
    result = ' '.join(pinyin)+' '+' '.join([email_prefix, birth, username])
    # result = ' '.join([email_prefix, birth, id, username, mobile])+' '+''.join(pinyin)
    dataset.append((result, pwd))
print(len(dataset))

output_file = r'D:\data\leak_final_20161219\12306_dataset.pkl'
pickle.dump(dataset, open(output_file, 'wb'))

paths = [r'D:\data\leak_final_20161219\pipw\train\all_pi-pw.pi.tok',
         r'D:\data\leak_final_20161219\pipw\train\all_pi-pw.pw.tok',
         r'D:\data\leak_final_20161219\pipw\dev\all_pi-pw.pi.tok',
         r'D:\data\leak_final_20161219\pipw\dev\all_pi-pw.pw.tok',
         r'D:\data\leak_final_20161219\pipw\test\all_pi-pw.pi.tok',
         r'D:\data\leak_final_20161219\pipw\test\all_pi-pw.pw.tok']

dirs = [r'D:\data\leak_final_20161219\pipw\train',
        r'D:\data\leak_final_20161219\pipw\dev',
        r'D:\data\leak_final_20161219\pipw\test']
[os.mkdir(dir) for dir in dirs if not os.path.exists(dir)]

ratios = [0.8, 0.9]

files = [codecs.open(path, 'w', encoding='utf-8') for path in paths]

max_len = 0
max_len_trg = 0
for data in dataset:
    info = data[0]
    final_info = []
    if data_aug:
        split_info = info.split()
        for shuffle_index in range(0, shuffle_cnt):
            random.shuffle(split_info)
            final_info.append(' '.join(split_info))
    else:
        final_info = [info]
    pwd = data[1]
    rng = random.random()
    if len(info) > max_len:
        max_len = len(info)
    if len(pwd) > max_len_trg:
        max_len_trg = len(pwd)
    if rng <= ratios[0]:
        for cur_info in final_info:
            files[0].writelines(cur_info + '\n')
            files[1].writelines(pwd + '\n')
    elif rng < ratios[1]:
        for cur_info in final_info:
            files[2].writelines(cur_info + '\n')
            files[3].writelines(pwd + '\n')
    else:
        for cur_info in final_info:
            files[4].writelines(cur_info + '\n')
            files[5].writelines(pwd + '\n')
[handler.flush() for handler in files]
[handler.close() for handler in files]
print(max_len)
print(max_len_trg)
