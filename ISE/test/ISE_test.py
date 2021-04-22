# -*- coding: utf-8 -*-
import time

from ise.main import ise_main

if __name__ == '__main__':
    t = -time.time()
    ise_main()
    t += time.time()
    print('ise_main run time:', t)
