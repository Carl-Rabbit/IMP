
from imm.main import *
from model.network import Network
from utils.utils import read_lines

# cnt_list = [
#     # 10,
#     # 50,
#     # 100,
#     # 500,
#     1000,
#     5000,
#     10000,
#     50000,
#     100000,
#     500000,
#     1000000,
#     5000000,
# ]

cnt_list = [5_0000 * i for i in range(1, 101)]

seed_cnt = 500

if __name__ == '__main__':
    network_lines = read_lines('../../DatasetOnTestPlatform/NetHEPT.txt')
    network: Network = Network(network_lines)

    create_workers(network.vs)

    for cnt in cnt_list:
        rrsets = []     # clear it
        t = -time.time()
        fill_rrsets(rrsets, cnt)
        t += time.time()
        print(f'fill_rrsets, {cnt}, {t}')

        t = -time.time()
        _ = node_selection(rrsets, seed_cnt)
        t += time.time()
        print(f'selection, {cnt}, {t}')

    terminate_workers()

    sys.stdout.flush()


"""
cnt_list = [
    # 10,
    # 50,
    # 100,
    # 500,
    1000,
    5000,
    10000,
    50000,
    100000,
    500000,
]

seed_cnt = 500

result:

sampling, 1000, 0.008012771606445312
selection, 1000, 0.11565494537353516
sampling, 5000, 0.03394961357116699
selection, 5000, 0.894599199295044
sampling, 10000, 0.05485796928405762
selection, 10000, 1.7283377647399902
sampling, 50000, 0.22140765190124512
selection, 50000, 8.176122903823853
sampling, 100000, 0.8467354774475098
selection, 100000, 17.394603967666626
sampling, 500000, 3.9833991527557373
selection, 500000, 99.25192546844482


cnt_list = [
    # 10,
    # 50,
    # 100,
    # 500,
    1000,
    5000,
    10000,
    50000,
    100000,
    500000,
    1000000,
    5000000,
]

seed_cnt = 500

fill_rrsets, 1000, 0.0069811344146728516
selection, 1000, 0.11768460273742676
fill_rrsets, 5000, 0.014000892639160156
selection, 5000, 0.7799084186553955
fill_rrsets, 10000, 0.03590273857116699
selection, 10000, 0.535599946975708
fill_rrsets, 50000, 0.1515958309173584
selection, 50000, 0.9125227928161621
fill_rrsets, 100000, 0.6004114151000977
selection, 100000, 0.9833719730377197
fill_rrsets, 500000, 2.7416276931762695
selection, 500000, 2.1283042430877686
fill_rrsets, 1000000, 4.952749252319336
selection, 1000000, 2.6409313678741455
fill_rrsets, 5000000, 30.996163606643677
selection, 5000000, 12.926073789596558
"""