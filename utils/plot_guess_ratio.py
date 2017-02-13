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
    cur_threshold = 1
    mul = 2
    rank_list = []
    guess_cnt = []
    pwd_cnt = 0
    for line in codecs.open(file_path, 'r', 'utf-8'):
        pieces = line.split('\t')
        rank = float(pieces[2])
        if rank > cur_threshold:
            rank_list.append(cur_threshold)
            guess_cnt.append(pwd_cnt)
            cur_threshold *= mul
        pwd_cnt += 1
    if rank <= cur_threshold:
        rank_list.append(cur_threshold)
        guess_cnt.append(pwd_cnt)

    rank_list = np.array(rank_list)
    guess_ratio = np.array(guess_cnt)/float(pwd_cnt)
    return rank_list, guess_ratio

file_lists = [r'D:\data\leak_final_20161219\pipw_1.0\pcfg_guess_number.txt',
              r'D:\data\leak_final_20161219\pipw_1.0\bpe2char_guess_number.txt']

labels = [u'PCFG',
          u'bpe2char']

styles = ['r--',
          'b-']

for idx, file_path in enumerate(file_lists):
    rank, ratio = gen_curve(file_path)
    plt.hold(True)
    plt.semilogx(rank, ratio, styles[idx], basex=10, label=labels[idx])
plt.grid(True)
plt.xlabel(u'猜测次数')
plt.ylabel(u'猜中比例')
plt.xlim([10**0, 10**8])
# plt.savefig(r'G:\workspace\python\dl4mt-c2c\result\figs\bpe2char_guess_number_ratio.jpg')
plt.legend()
plt.show()
