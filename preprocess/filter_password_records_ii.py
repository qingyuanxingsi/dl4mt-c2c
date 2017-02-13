# -*- coding:utf-8 -*-

local_file_1 = r'D:\data\leak_final_20161219\pipw_1.0\test\all_pi-pw.pi.tok'
local_file_2 = r'D:\data\leak_final_20161219\pipw_1.0\test\all_pi-pw.pw.tok'

output_file_1 = open(r'D:\data\leak_final_20161219\pipw_1.0\test\all_pi-pw.pi.tok2', 'w')
output_file_2 = open(r'D:\data\leak_final_20161219\pipw_1.0\test\all_pi-pw.pw.tok2', 'w')

feat_list = list()
pwd_list = list()

for line in open(local_file_1):
    feat_list.append(line)

for line in open(local_file_2):
    pwd_list.append(line)

pwd_set = set()
for idx, pwd in enumerate(pwd_list):
    if pwd not in pwd_set:
        pwd_set.add(pwd)
        output_file_1.writelines(feat_list[idx])
        output_file_2.writelines(pwd)

output_file_1.flush()
output_file_1.close()
output_file_2.flush()
output_file_2.close()

