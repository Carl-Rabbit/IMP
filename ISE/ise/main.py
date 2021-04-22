# -*- coding: utf-8 -*-
# written by mark zeng 2018-11-14
# modified by Yao Zhao 2019-10-30
# re-modified by Yiming Chen 2020-11-04

import multiprocessing as mp
import random
import time
import sys
import argparse
from typing import List

import numpy as np

from ise.ic import ic_sample
from ise.lt import lt_sample
from ise.network import init_network, init_seed_set
from ise.util import read_lines

CORE = 8
TIME_LEFT = 6


def ise_main():
    file_name, seed_name, model, time_limit = param_parse()
    timestamp_limit = time.time() + time_limit - TIME_LEFT

    # print('Params:', file_name, seed_name, model, time_limit)

    network_lines = read_lines(file_name)
    seed_lines = read_lines(seed_name)

    raw_result = run(network_lines, seed_lines, model, timestamp_limit)

    print(get_avg(raw_result))

    sys.stdout.flush()


class TimeoutException(Exception):
    def __init__(self, msg):
        self.msg = msg


def param_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-s', '--seed', type=str, default='seeds.txt')
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()
    file_name = args.file_name
    seed = args.seed
    model = args.model
    time_limit = args.time_limit

    return file_name, seed, model, time_limit


def run(network_lines, seed_lines, model, timestamp_limit):
    result_list = []
    pool = mp.Pool(CORE)

    if model == 'IC':
        func = ic_sample
    elif model == 'LT':
        func = lt_sample
    else:
        raise Exception('model type error')

    try:
        for i in range(CORE):
            args = (network_lines, seed_lines, func, timestamp_limit)
            result_list.append(pool.apply_async(sample_algo, args=args))
        pool.close()
        pool.join()
    except TimeoutException as e:
        print(e.msg)
    finally:
        pool.terminate()

    return result_list


def sample_algo(network_lines, seed_lines, sample_func, timestamp_limit):
    network = init_network(network_lines)
    network_lines = None
    seed_set = init_seed_set(seed_lines, network)
    seed_lines = None
    res_sum = 0
    res_cnt = 0

    np.random.seed(random.randint(0, 19260817))

    while True:
        res = sample_func(network, seed_set, timestamp_limit)
        if res:
            res_sum += res
            res_cnt += 1
        else:
            break
    return res_sum, res_cnt


def get_avg(raw_result):
    tot_sum, tot_cnt = 0, 0
    for sum_, cnt in [res.get() for res in raw_result]:
        # print(sum_, cnt)
        tot_sum += sum_
        tot_cnt += cnt
    # print('tot_cnt:', tot_cnt)
    avg = -1 if tot_cnt == 0 else tot_sum / tot_cnt
    return avg
