# -*- coding:utf-8 -*-
import codecs
import math
import numpy as np
import matplotlib.pyplot as plt

from pylab import *
# 指定默认字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False


def gen_curve(file_path):
    """
    Generate rank_list and guess_ratio by file path
    :param file_path:
    :return:
    """
    prev_rank = 0
    rank_list = []
    guess_cnt = []
    pwd_cnt = 0
    cur_cnt = 0
    for line in codecs.open(file_path, 'r', 'utf-8'):
        pieces = line.split('\t')
        rank = float(pieces[2])
        if rank != prev_rank:
            if cur_cnt != 0:
                rank_list.append(prev_rank)
                guess_cnt.append(pwd_cnt)
                cur_cnt = 0
            prev_rank = rank
        cur_cnt += 1
        pwd_cnt += 1
    if cur_cnt != 0:
        rank_list.append(prev_rank)
        guess_cnt.append(pwd_cnt)

    rank_list = np.array(rank_list)
    guess_ratio = np.array(guess_cnt)/float(pwd_cnt)
    return rank_list, guess_ratio, pwd_cnt

file_lists = [r'D:\data\leak_final_20161219\pipw_1.0\pcfg_guess_number.txt',
              r'D:\data\leak_final_20161219\pipw_1.0\bpe2char_guess_number.txt']

labels = [u'PCFG',
          u'bpe2char']

for idx, file_path in enumerate(file_lists):
    rank, ratio, cnt = gen_curve(file_path)
    plt.hold(True)
    plt.semilogx(rank, ratio, basex=10, label=labels[idx])

plt.grid(True)
plt.xlabel(u'猜测次数')
plt.ylabel(u'猜中比例')
plt.xlim([10**0, 10**8])
# plt.savefig(r'D:\data\leak_final_20161219\pipw_1.0\pcfg_guess_number_ratio.jpg')
plt.legend()
plt.show()
