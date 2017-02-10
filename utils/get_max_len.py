# -*- coding:utf-8 -*-
import codecs

local_file = r'D:\data\leak_final_20161219\pipw\train\all_pi-pw.pi.tok.bpe'

line_cnt = 0
max_len = 0
for line in codecs.open(local_file, 'r', 'utf-8'):
    pieces = line.strip().split()
    cur_len = len(pieces)
    if cur_len > max_len:
        max_len = cur_len
    line_cnt += 1
print("Line count:%d" % line_cnt)
print("Max Len:%d" % max_len)
