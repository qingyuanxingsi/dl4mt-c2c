import argparse
import sys
import os
import time

reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.insert(0, "/home/lanlin/workspace/dl4mt-c2c/bpe2char")  # change appropriately

import numpy
import cPickle as pkl
from mixer import *
from data_iterator import TextIterator
import random
import theano
import math


# python evaluate/bpe2char_meter_evaluate.py -model /home/lanlin/workspace/dl4mt-c2c/models/pi_pwbi-bpe2char.grads.370000.npz -saveto /home/lanlin/workspace/dl4mt-c2c/result/bpe2char_370000_test.txt -translate pi_pw


def main(model, src_dict, target_dict, source_file, target_file, saveto,
         source_word_level=1,
         target_word_level=0,
         valid_batch_size=128,
         n_words_src=302,
         n_words=302):
    from char_base import (init_params, build_model, build_sampler)
    from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
    from nmt import (pred_probs, prepare_data)

    # load model model_options
    pkl_file = model.split('.')[0] + '.pkl'
    with open(pkl_file, 'rb') as f:
        options = pkl.load(f)

    trng = RandomStreams(1234)

    # allocate model parameters
    params = init_params(options)

    # load model parameters and set theano shared variables
    params = load_params(model, params)

    # create shared variables for parameters
    tparams = init_tparams(params)

    trng, use_noise, \
    x, x_mask, y, y_mask, \
    opt_ret, \
    cost = \
        build_model(tparams, options)
    inps = [x, x_mask, y, y_mask]

    print 'Building sampler...\n',
    f_init, f_next = build_sampler(tparams, options, trng, use_noise)
    print 'Done'

    # before any regularizer
    print 'Building f_log_probs...',
    f_log_probs = theano.function(inps, cost)
    print 'Done'

    print('Preparing dataset...')
    dataset = TextIterator(source=source_file,
                           target=target_file,
                           source_dict=src_dict,
                           target_dict=target_dict,
                           n_words_source=n_words_src,
                           n_words_target=n_words,
                           source_word_level=source_word_level,
                           target_word_level=target_word_level,
                           batch_size=valid_batch_size,
                           sort_size=sort_size)

    print('Predicting probs...')
    log_probs = pred_probs(f_log_probs, prepare_data,
                           options, dataset, verboseFreq=10000)
    print('Done...')
    output_file = open(saveto, 'w')
    pwd_cnt = 0
    for line in open(target_file):
        output_file.writelines(line.rstrip()+'\t'+str(1.0/(math.e**log_probs[pwd_cnt]))+'\n')
        pwd_cnt += 1
    """
    for prob in log_probs:
        output_file.writelines(str(prob) + '\n')
    """
    output_file.flush()
    output_file.close()
    print('Evaluation finished...')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    """
    parser.add_argument('-utf8', action="store_true", default=True)
    parser.add_argument('-silent', action="store_true", default=False)  # suppress progress messages
    """
    parser.add_argument('-model', type=str)  # absolute path to a model (.npz file)
    parser.add_argument('-translate', type=str, help="de_en / cs_en / fi_en / ru_en / pi_pw")  # which language?
    parser.add_argument('-saveto', type=str)  # absolute path where the translation should be saved
    parser.add_argument('-which', type=str, help="dev / test1 / test2", default="test2")
    parser.add_argument('-sort_size', type=int, default=20, help="")
    parser.add_argument('-source_word_level', type=int, default=1, help="")
    parser.add_argument('-target_word_level', type=int, default=0, help="")
    parser.add_argument('-valid_batch_size', type=int, default=128, help="")
    parser.add_argument('-n_words_src', type=int, default=302, help="298 for FI")
    parser.add_argument('-n_words', type=int, default=302, help="292 for FI")
    # if you wish to translate any of development / test1 / test2 file from WMT15,
    # simply specify which one here
    parser.add_argument('-source', type=str,
                        default="")
    # if you wish to provide your own file to be translated, provide an absolute path to the file to be translated
    parser.add_argument('-target', type=str,
                        default="")

    args = parser.parse_args()

    data_path = "/home/lanlin/workspace/data/"

    if args.which not in "dev test1 test2".split():
        raise Exception('No corresponding dataset...')

    if args.translate not in ["de_en", "cs_en", "fi_en", "ru_en", "pi_pw"]:
        raise Exception('No corresponding language pair')

    if args.translate == "fi_en" and args.which == "test2":
        raise Exception('1')

    from wmt_path import *

    aa = args.translate.split("_")
    lang = aa[0]
    en = aa[1]

    version = 'pipw_1.0'
    dictionary = "%s/train/all_%s-%s.%s.tok.bpe.word.pkl" % (version, lang, en, lang)
    dictionary_target = "%s/train/all_%s-%s.%s.tok.302.pkl" % (version, lang, en, en)
    # dictionary = "%s%s/train/all_%s-%s.%s.tok.bpe.word.pkl" % (lang, en, lang, en, lang)
    # dictionary_target = "%s%s/train/all_%s-%s.%s.tok.300.pkl" % (lang, en, lang, en, en)
    source = wmts[args.translate][args.which][1][0]
    target = wmts[args.translate][args.which][0][1]

    # /work/yl1363/bpe2char/de_en/deen_bpe2char_two_layer_gru_decoder_adam.grads.355000.npz
    model_id = args.model.split('/')[-1]

    dictionary = data_path + dictionary
    dictionary_target = data_path + dictionary_target
    source = data_path + source
    target = data_path + target
    sort_size = args.sort_size

    if args.source != "":
        source = args.source

    if args.target != "":
        target = args.target

    n_words_dic = {'de_en': [24254, 302],
                   'cs_en': [21816, 302],
                   'fi_en': [20783, 292],
                   'ru_en': [22106, 302],
                   'pi_pw': [3166, 97]}

    args.n_words_src = n_words_dic[args.translate][0]
    args.n_words = n_words_dic[args.translate][1]

    print "src dict:", dictionary
    print "trg dict:", dictionary_target
    print "source:", source
    print "target:", target

    print "dest :", args.saveto

    print args

    time1 = time.time()
    main(args.model, dictionary, dictionary_target, source, target, args.saveto,
         source_word_level=args.source_word_level,
         target_word_level=args.target_word_level,
         valid_batch_size=args.valid_batch_size,
         n_words_src=args.n_words_src,
         n_words=args.n_words)
    time2 = time.time()
    duration = (time2 - time1) / float(60)
    print("Evaluation took %.2f minutes" % duration)
