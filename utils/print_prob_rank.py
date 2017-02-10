# -*- coding:utf-8 -*-

import pickle

pkl_file = r'G:\workspace\python\dl4mt-c2c\result\pcfg.pkl'

prob_list, rank_list = pickle.load(open(pkl_file, 'rb'))

print(prob_list[500])
print(rank_list[500])
