import random
import sys
import time
from typing import List

from imm.ic import get_ic_rrset
from imm.lt import get_lt_rrset
from model.network import Network
from utils.utils import param_parse
from utils.utils import write_lines

CORE = 1
TIME_LEFT = 10

MEM_LIMIT = 750 * (2 ** 20)
SIZE_LIMIT = 800_0000
PHARSE_NUM = 128

INIT_E = 0.1
INIT_L = 1

rrset_func = get_ic_rrset

start_time: float
time_limit: float

heap: List[List]
top_idx: int


def imm_main():
    global start_time, time_limit

    file_name, seed_cnt, model, time_limit = param_parse()

    # time_limit *= 10      # for test

    start_time = time.time()

    # print_tmp('Params:', file_name, seed_cnt, model, time_limit)

    # network_lines = read_lines(file_name)
    # run(network_lines, seed_cnt, model)

    network = Network()
    with open(file_name, 'r') as fp:
        network.parse_first_line(fp.readline())
        for _ in range(network.m):
            network.parse_data_line(fp.readline())
    run(None, seed_cnt, model, network)

    sys.stdout.flush()
    print('time cost: ', time.time() - start_time)


def run(network_lines, k, model, network_input=None):
    global rrset_func, heap, top_idx

    if model == 'IC':
        rrset_func = get_ic_rrset
    elif model == 'LT':
        rrset_func = get_lt_rrset
    else:
        raise Exception('model type error')

    network: Network

    if network_input:
        network = network_input
    else:
        network = Network(network_lines)

    # step 1
    # t0 = time.time()
    # rrsets: List[Set] = sampling(network, k, e, l)
    rrsets: List[List] = sampling(network, k, model)

    del network

    # step 2
    # print(f'len(rrsets) = {len(rrsets)}')

    # t1 = time.time()
    # init vtx2sid_lst
    vtx2sid_list = get_vtx2sid_lst(rrsets)
    del rrsets

    # init heap
    init_heap(vtx2sid_list)
    del vtx2sid_list

    # t2 = time.time()

    # node selection
    seeds = node_selection(k)
    # t3 = time.time()

    # print(f'sampling: {t1 - t0}\ninit heap: {t2 - t1}\nselection: {t3 - t2}')

    # remember to + 1 because I store the index begin at 0
    output_lst = [str(i + 1) for i in seeds]
    print('\n'.join(output_lst))

    print('write to test folder')
    write_lines('../DatasetOnTestPlatform/my_' + str(model).lower() + '_seeds.txt', output_lst)


def get_vtx2sid_lst(rrsets: List[List]):
    vtx2sid_lst = {}
    sid = 0
    for rrset in rrsets:
        for vid in rrset:
            if vid not in vtx2sid_lst:
                vtx2sid_lst[vid] = [sid]
            else:
                vtx2sid_lst[vid].append(sid)
        sid += 1
        del rrset
    return vtx2sid_lst


def init_heap(vtx2sid_lst: dict):
    global top_idx, heap

    top_idx = len(vtx2sid_lst) + 1
    heap = [[] for _ in range(top_idx)]       # max heap for [vid, score, sid_lst]

    idx = len(heap) - 1
    for vid, sid_lst in vtx2sid_lst.items():
        score = len(sid_lst)
        heap[idx] += [vid, score, sid_lst]
        shift_down(idx)
        idx -= 1


def sampling(network: Network, k, model) -> List[List]:
    global start_time, time_limit, MEM_LIMIT, SIZE_LIMIT, rrset_func

    rrsets: List[List] = []

    time_for_sampling = 0.70 * (time_limit - TIME_LEFT)

    if network.n > 8_0000:
        # deal with large graph
        time_for_sampling = 0.60 * (time_limit - TIME_LEFT)
        MEM_LIMIT *= 0.8
    elif network.n > 3_5000:
        MEM_LIMIT *= 1.0
    elif network.n < 2_0000:
        MEM_LIMIT *= 1.2

    if model == 'LT' and network.n > 2_0000:
        MEM_LIMIT *= 0.7
        SIZE_LIMIT *= 0.7
        time_for_sampling *= 0.67

    # print('time_for_sampling = ', time_for_sampling)

    time_bound = start_time + time_for_sampling

    vs, n = network.vs, network.n

    total_size = 0
    rrsets_size = 0
    unit = 0

    timer = 0

    while True:
        r = int(random.random() * n)
        rrset = rrset_func(vs, r)
        rrsets.append(rrset)
        if timer:
            if total_size >= MEM_LIMIT or time.time() > time_bound:
                break
            unit = sys.getsizeof(rrset)
            total_size -= rrsets_size
            rrsets_size = sys.getsizeof(rrsets)
            total_size += rrsets_size
        timer += 1
        timer %= 16
        total_size += unit

    # print(f'size target = {MEM_LIMIT / 2 ** 20}, '
    #       f'act = {sum([sys.getsizeof(rrset) for rrset in rrsets]) / 2 ** 20}, '
    #       f'statistics = {total_size}')

    return rrsets


def shift_down(i):
    global top_idx, heap

    while True:
        left_idx = 2 * i
        if left_idx >= top_idx:
            return
        right_idx = 2 * i + 1
        if right_idx >= top_idx:
            max_idx = left_idx
        else:
            if heap[left_idx][1] > heap[right_idx][1]:
                max_idx = left_idx
            else:
                max_idx = right_idx

        if heap[i][1] >= heap[max_idx][1]:
            return

        heap[i], heap[max_idx] = heap[max_idx], heap[i]

        i = max_idx


def node_selection(k):
    """
    Greedy select k nodes from rrsets
    :param k: the size of return set
    :return: the vertexes that we select (Sk)
    """
    global top_idx, heap

    s_k = []

    seed_cnt = 0
    covered_set = set()
    while seed_cnt < k:
        lst = heap[1]
        new_sid_lst = list(filter(lambda e: e not in covered_set, lst[2]))
        new_score = len(new_sid_lst)
        lst[1], lst[2] = new_score, new_sid_lst

        if new_score >= max(heap[2][1], heap[3][1]):
            vid = lst[0]

            top_idx -= 1
            heap[1] = heap[top_idx]
            shift_down(1)

            s_k.append(vid)
            seed_cnt += 1

            for sid in new_sid_lst:
                covered_set.add(sid)
        else:
            shift_down(1)

    return s_k
