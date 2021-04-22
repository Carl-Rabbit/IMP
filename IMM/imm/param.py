import math

import numpy as np

LOG2 = np.log(2)


def get_lamb_p(n, k, ep, l) -> float:
    """ Get lambda' """
    return (2 + 2 / 3 * ep) * (get_logc(n, k) + l * np.log(n) + np.log(np.log2(n))) * n / (ep * ep)


def get_logc(n, k) -> float:
    """ Get log(C(n, k)) """
    lst1 = [n - i for i in range(k)]
    lst2 = [i for i in range(2, k + 1)]
    return sum(np.log(lst1)) - sum(np.log(lst2))


def get_lamb_s(n, k, e, l) -> float:
    """ Get lambda* """
    alpha = np.sqrt(l * np.log(n) + LOG2)
    beta = np.sqrt(
        (1 - 1 / np.e)
        * (get_logc(n, k) + l * np.log(n) + LOG2)
    )
    return 2 * n * (((1 - 1 / np.e) * alpha + beta) ** 2) * (e ** -2)
