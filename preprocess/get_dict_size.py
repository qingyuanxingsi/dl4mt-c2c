# -*- coding:utf-8 -*-

import pickle

local_file = r'D:\data\leak_final_20161219\12306_leak.pkl'
data = pickle.load(open(local_file, 'rb'))
print(len(data))
