# -*- coding:utf-8 -*-
import pickle


def bi_search(prob, prob_list):
    """
    Binary search the probability list to
    find the corresponding rank
    find last prob_list[index] > prob
    :param prob:
    :param prob_list:
    :return:
    """
    # 1.0 0.8 0.7 0.7 0.7 0.6 0.0
    # 0.7
    # 0 4 2
    # 2 4 3
    # 2 2
    prob_len = prob_list.shape[0]
    start_index = 0
    end_index = prob_len-1
    while start_index < end_index-1:
        mid = (start_index + end_index)//2
        cur_prob = prob_list[mid]
        if cur_prob > prob:
            start_index = mid
        else:
            end_index = mid-1
    if prob_list[end_index] > prob:
        return end_index
    return start_index

if __name__ == '__main__':
    local_file = r'G:\workspace\python\dl4mt-c2c\result\pcfg.pkl'
    prob_list, rank_list = pickle.load(open(local_file, 'rb'))
    idx = bi_search(0.001, prob_list)
    print(prob_list[idx:idx+5])
    print(rank_list[idx:idx+5])




