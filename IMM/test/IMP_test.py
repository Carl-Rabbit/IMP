# -*- coding: utf-8 -*-
import time

from imm.main import imm_main

if __name__ == '__main__':
    t = -time.time()
    imm_main()
    t += time.time()
    print('imm_main run time:', t)
