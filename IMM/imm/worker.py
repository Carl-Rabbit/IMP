import multiprocessing as mp
import random
import sys
import time

import numpy as np


class Worker(mp.Process):

    def __init__(self, wid, in_q, out_q, vs, rrset_func):
        super(Worker, self).__init__(target=self.start)
        self.wid = wid
        self.in_q = in_q
        self.out_q = out_q
        self.vs = vs
        self.rrset_func = rrset_func

        seed = time.time_ns() % (2 ** 30)
        np.random.seed(seed)
        random.seed(seed)

    def run(self):
        n = len(self.vs)

        time_limit, pharse_num, mem_limit, size_limit = self.in_q.get()
        # print(f'id = {self.wid}, time_limit = {time_limit}, rrset_limit = {rrset_limit}')

        # run one pharse

        pharse_size, target_pharse_size = 0, int(mem_limit / pharse_num)
        buffer = []

        while pharse_size <= target_pharse_size:
            r = int(random.random() * n)
            rrset = self.rrset_func(self.vs, r)
            if rrset:
                buffer.append(rrset)
                pharse_size += sys.getsizeof(rrset)

        self.out_q.put((0, buffer))

        # run left

        rrset_cnt_for_one_pharse = min(size_limit / pharse_num, len(buffer))
        left_pharse_num = pharse_num - 1

        del buffer

        while time.time() < time_limit and left_pharse_num > 0:
            left_pharse_num -= 1

            count = 0
            buffer = []

            while count < rrset_cnt_for_one_pharse:
                r = int(random.random() * n)
                rrset = self.rrset_func(self.vs, r)
                if rrset:
                    buffer.append(rrset)
                    count += 1

            self.out_q.put((0, buffer))
            del buffer

        self.out_q.put((-1, None))
