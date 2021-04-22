import time
from random import random

import numpy


def python_random(count):
    lst = [0] * count

    t = -time.time_ns()
    for i in range(count):
        lst[i] = random()
    t += time.time_ns()

    return lst, t / 10 ** 6, t / count / 10 ** 6


def np_random(count):
    lst = [0] * count

    t = -time.time_ns()
    for i in range(count):
        lst[i] = numpy.random.rand()
    t += time.time_ns()

    return lst, t / 10 ** 6, t / count / 10 ** 6


def npn_random(count):
    t = -time.time_ns()
    lst = numpy.random.random(count)
    t += time.time_ns()

    return lst, t / 10 ** 6, t / count / 10 ** 6


def np_uniform_random(count):
    t = -time.time_ns()
    lst = numpy.random.uniform(count)
    t += time.time_ns()

    return lst, t / 10 ** 6, t / count / 10 ** 6


if __name__ == '__main__':
    count = 1000000
    print('count=', count)
    print('for + random.random():', python_random(count)[1:])
    print('for + numpy.random.rand():', np_random(count)[1:])
    print('numpy.random.random(size):', npn_random(count)[1:])
    print('numpy.random.uniform(size):', npn_random(count)[1:])
