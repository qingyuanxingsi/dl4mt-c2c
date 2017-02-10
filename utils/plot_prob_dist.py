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

local_file = r'D:\data\leak_final_20161219\result\char2char_85000_result.txt'

max_bins = 128
probs = np.zeros((max_bins,))
whole_cnt = 0
for line in codecs.open(local_file, 'r', 'utf-8'):
    whole_cnt += 1
    pieces = line.split('----')
    sample = pieces[0]
    log_prob = float(pieces[1])
    prob = 1./(math.e**log_prob)
    cur_bin = int(np.floor(np.abs(np.log2(prob))))
    if cur_bin >= max_bins:
        continue
    probs[cur_bin] += 1

probs /= whole_cnt

bar_width = 0.8
x = np.linspace(0, max_bins-1, max_bins)*bar_width
plt.bar(x, probs, width=bar_width)
plt.xlabel(u'概率区间')
plt.ylabel(u'概率')
plt.title(u'char2char密码样本概率分布')
plt.grid(True)
plt.savefig(r'G:\workspace\python\dl4mt-c2c\result\figs\char2char_sample_prob_distribution.jpg')
plt.show()