__author__ = 'apple'
import pickle

local_file = r'D:\data\leak_final_20161219\12306_dataset.pkl'

dict = pickle.load(open(local_file, 'rb'))

print(len(dict))

# 2136 2190
# 70 76
