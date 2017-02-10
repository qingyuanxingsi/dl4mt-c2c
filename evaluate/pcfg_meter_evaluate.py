# -*- coding:utf-8 -*-

import os
import codecs
import numpy as np
import re


class PCFGMeter:
    def __init__(self, pcfg_dir, dics):
        print('Building PCFG Meter...')
        self.digit_dict = dict()
        self.special_dict = dict()
        self.grammar_dict = dict()
        self.letter_cnt_dict = dict()
        self.letter_prob_dict = dict()
        self.digit_regex = re.compile('[0-9]')
        self.letter_regex = re.compile('[a-zA-Z]')
        self.special_regex = re.compile('[^a-zA-Z0-9]')
        if not os.path.exists(pcfg_dir):
            raise Exception('PCFG directory do not exist...')
        digit_dir = os.path.join(pcfg_dir, 'digits')
        for digit_file in os.listdir(digit_dir):
            digit_file_path = os.path.join(digit_dir, digit_file)
            for line in codecs.open(digit_file_path, 'r', 'utf-8'):
                pieces = line.split('\t')
                cur_digit = pieces[0]
                cur_prob = float(pieces[1])
                self.digit_dict[cur_digit] = cur_prob
        special_dir = os.path.join(pcfg_dir, 'special')
        for special_file in os.listdir(special_dir):
            special_file_path = os.path.join(special_dir, special_file)
            for line in codecs.open(special_file_path, 'r', 'utf-8'):
                pieces = line.split('\t')
                cur_special = pieces[0]
                cur_prob = float(pieces[1])
                self.special_dict[cur_special] = cur_prob
        grammer_file = os.path.join(pcfg_dir, 'grammar/structures.txt')
        for line in codecs.open(grammer_file, 'r', 'utf-8'):
            pieces = line.split()
            cur_grammar = pieces[0]
            cur_prob = float(pieces[1])
            self.grammar_dict[cur_grammar] = cur_prob
        for dic in dics:
            for line in codecs.open(dic, 'r', 'utf-8'):
                str_len = len(line.strip())
                if str_len not in self.letter_cnt_dict:
                    self.letter_cnt_dict[str_len] = 1
                else:
                    self.letter_cnt_dict[str_len] += 1
        for key, value in self.letter_cnt_dict.items():
            self.letter_prob_dict[key] = 1.0/value

    def compute_prob(self, pwd):
        """
        Compute probability for the password
        :param pwd:
        :return:
        """
        final_prob = 1.0
        tmp_1 = re.sub(self.letter_regex, 'L', pwd)
        tmp_2 = re.sub(self.digit_regex, 'D', tmp_1)
        pwd_structure = re.sub(self.special_regex, 'S', tmp_2)
        if pwd_structure not in self.grammar_dict:
            return 0.0, False
        struct_prob = self.grammar_dict[pwd_structure]
        final_prob *= struct_prob
        pre = ''
        seg = ''
        final_segs = []
        for index in range(0, len(pwd_structure)):
            cur = pwd_structure[index]
            if cur == pre:
                seg += pwd[index]
            else:
                if len(seg) != 0:
                    final_segs.append(seg)
                    seg = ''
                seg += pwd[index]
                pre = cur
        if len(seg) != 0:
            final_segs.append(seg)
        for cur_seg in final_segs:
            cur_seg = str(cur_seg)
            if str.isdigit(cur_seg):
                if cur_seg not in self.digit_dict:
                    return 0.0, False
                final_prob *= self.digit_dict[cur_seg]
            elif str.isalpha(cur_seg):
                if len(cur_seg) not in self.letter_prob_dict:
                    return 0.0, False
                final_prob *= self.letter_prob_dict[len(cur_seg)]
            else:
                if cur_seg not in self.special_dict:
                    return 0.0, False
                final_prob *= self.special_dict[cur_seg]
        return final_prob, True

    def gen_prob(self, test_file, output_file_path, max_cnt=20000000):
        """
        Generate probability for the test set passwords
        :param test_file:
        :param output_file_path:
        :return:
        """
        print('Generate probs...')
        output_file = codecs.open(output_file_path, 'w', 'utf-8')
        cur_cnt = 0
        for line in codecs.open(test_file, 'r', 'utf-8'):
            cur_cnt += 1
            if cur_cnt > max_cnt:
                break
            pwd = line.strip()
            prob, ok = self.compute_prob(pwd)
            if ok:
                output_file.writelines(pwd+'\t'+str(prob)+'\n')
        output_file.flush()
        output_file.close()

if __name__ == '__main__':
    pcfg_meter = PCFGMeter(r'D:\data\leak_final_20161219\pcfg_pipw_1.0',
                           [r'D:\data\leak_final_20161219\pcfg_pipw_1.0\dics\dic-0294.txt'])
    pcfg_meter.gen_prob(r'D:\data\leak_final_20161219\pipw_1.0\test\pwd_unique_test.txt',
                        r'D:\data\leak_final_20161219\pipw_1.0\test\pcfg_test_probs.txt')






