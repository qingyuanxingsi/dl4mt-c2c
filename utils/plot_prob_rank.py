# -*- coding:utf-8 -*-
import codecs
import math
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

from pylab import *
# 指定默认字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False


def gen_curve(file_path, method='demo'):
    """
    Generate prob_list and rank_list by file path
    :param file_path:
    :param method:
    :return:
    """
    prob_threshold = 2**(-30)
    pwd_list = []
    prob_list = []
    for line in codecs.open(file_path, 'r', 'utf-8'):
        # pieces = line.split('----')
        # sample = pieces[0]
        # log_prob = float(pieces[1])
        log_prob = float(line.strip())
        prob = 1.0/(math.e**log_prob)
        if prob < prob_threshold:
            continue
        pwd_list.append(sample)
        prob_list.append(prob)

    # sorting the probs in descending order
    prob_list = np.array(prob_list)
    sort_indice = np.argsort(-prob_list)
    pwd_list = [pwd_list[index] for index in sort_indice]
    prob_list = prob_list[sort_indice]

    sample_len = len(pwd_list)
    print(sample_len)

    rank_list = np.zeros((sample_len,), dtype=np.float64)
    rank_list[0] = 1./(sample_len**prob_list[0])

    for index in range(1, sample_len):
        rank_list[index] = rank_list[index-1] + 1./(sample_len*prob_list[index])
    output_file_path = os.path.join(r'G:\workspace\python\dl4mt-c2c\result', method+'.pkl')
    pickle.dump([prob_list, rank_list], open(output_file_path, 'wb'))
    return prob_list, rank_list

"""
methods = ['bpe2char', 'pcfg', 'char2char']
file_lists = [r'D:\data\leak_final_20161219\result\bpe2char_85000_result.txt',
              r'D:\data\leak_final_20161219\pcfg\result\pcfg_probs.txt',
              r'D:\data\leak_final_20161219\result\char2char_85000_result.txt']
labels = [u'bpe2char',
          u'PCFG',
          u'char2char']

styles = ['r--',
          'b-',
          'k:']
"""
methods = ['pcfg']
file_lists = [r'D:\data\leak_final_20161219\pcfg\pcfg_guesses_probs.txt']
labels = [u'PCFG']
styles = ['r--']

probs = []
ranks = []
for file_index, file_path in enumerate(file_lists):
    prob, rank = gen_curve(file_path, method=methods[file_index])
    probs.append(prob)
    ranks.append(rank)

file_len = len(file_lists)
for gen_index in range(0, file_len):
    cur_prob = probs[gen_index]
    cur_rank = ranks[gen_index]
    plt.hold(True)
    plt.loglog(cur_prob, cur_rank, styles[gen_index], basex=2, basey=2, label=labels[gen_index])
cur_xticks = [2**x_tick for x_tick in range(-30, -4, 2)]
cur_yticks = [2**y_tick for y_tick in range(0, 15, 2)]
plt.xticks(cur_xticks)
plt.yticks(cur_yticks)
plt.xlim([2**(-30), 2**(-6)])
plt.ylim([2**0, 2**12])
plt.gca().invert_xaxis()
plt.grid(True)
plt.xlabel(u'概率')
plt.ylabel(u'猜测次数')
plt.title(u'概率-猜测次数')
plt.legend(loc='upper left')
plt.savefig(r'G:\workspace\python\dl4mt-c2c\result\figs\prob_rank_pcfg.jpg')
plt.show()