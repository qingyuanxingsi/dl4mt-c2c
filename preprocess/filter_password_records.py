# -*- coding:utf-8 -*-

local_file = r'D:\data\leak_final\pipw_1.0\dev\all_pi-pw.pw.tok'
out_file = open(r'D:\data\leak_final\pipw_1.0\dev\pwd_unique_dev.txt', 'w')

pwd_set = set()
pwd_cnt = 0
for line in open(local_file):
    pwd = line.rstrip()
    if pwd not in pwd_set:
        out_file.writelines(pwd+"\n")
        pwd_set.add(pwd)
        pwd_cnt += 1

print(pwd_cnt)
out_file.flush()
out_file.close()
