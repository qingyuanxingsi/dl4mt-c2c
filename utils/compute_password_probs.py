# -*- coding:utf-8 -*-

import math

local_file = r'D:\data\leak_final_20161219\pipw_1.0\bpe2char_95000_test.txt'
out_file = open(r'D:\data\leak_final_20161219\pipw_1.0\bpe2char_test_result.txt', 'w')

"""
for line in open(local_file):
    pieces = line.strip().split('----')
    pwd = pieces[0]
    score = float(pieces[1])
    prob = 1.0/(math.e**score)
    result = [pwd, str(prob)]
    out_file.writelines('\t'.join(result)+'\n')
"""
for line in open(local_file):
    score = float(line.strip())
    prob = 1.0/(math.e**score)
    out_file.writelines('test'+'\t'+str(prob)+'\n')

out_file.flush()
out_file.close()
