import random
import time

if __name__ == '__main__':
    random.seed(time.time())
    vertex_num = 60000
    edge_num = 600000
    # seed_num = 6000
    # assert seed_num <= vertex_num
    #
    # out = open('DatasetOnTestPlatform/seed_6000_1.txt', 'w')
    # seed_set = set()
    # for i in range(seed_num):
    #     new_seed = random.randint(0, vertex_num - 1)
    #     while new_seed in seed_set:
    #         new_seed = random.randint(0, vertex_num - 1)
    #     seed_set.add(new_seed)
    # for seed in seed_set:
    #     out.write('{}\n'.format(seed))
    # out.flush()
    # out.close()

    edges = []
    vertex_in_edge_count = {}
    for i in range(edge_num):
        source = random.randint(0, vertex_num - 1)
        dest = random.randint(0, vertex_num - 1)
        while dest == source:
            dest = random.randint(0, vertex_num - 1)
        edges.append([source, dest, 0.0])
    for edge in edges:
        dest = edge[1]
        if dest not in vertex_in_edge_count:
            vertex_in_edge_count[dest] = 0
        vertex_in_edge_count[dest] += 1
    for edge in edges:
        dest = edge[1]
        edge[2] = 1.0 / vertex_in_edge_count[dest]
    out = open(f'../DatasetOnTestPlatform/in_{vertex_num}_{edge_num}_1.txt', 'w')
    out.write('{} {}\n'.format(vertex_num, edge_num))
    for edge in edges:
        out.write('{} {} {}\n'.format(edge[0], edge[1], edge[2]))
    out.flush()
    out.close()
