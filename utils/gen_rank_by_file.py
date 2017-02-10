# -*- coding:utf-8 -*-

import pickle
import codecs
import math
from gen_guess_rank import bi_search

test_file = r'D:\data\leak_final_20161219\pcfg\pcfg_test_probs.txt'

pkl_file = r'G:\workspace\python\dl4mt-c2c\result\pcfg.pkl'
output_file_path = r'D:\data\leak_final_20161219\pcfg\pcfg_test_rank.txt'
output_file = codecs.open(output_file_path, 'w', 'utf-8')

prob_list, rank_list = pickle.load(open(pkl_file, 'rb'))

for line in codecs.open(test_file, 'r', 'utf-8'):
    log_prob = float(line.strip())
    cur_prob = 1/(math.e**log_prob)
    idx = bi_search(cur_prob, prob_list)
    cur_rank = rank_list[idx]
    final_result = [str(cur_prob), str(cur_rank)]
    output_file.writelines('----'.join(final_result)+'\n')
output_file.flush()
output_file.close()


