from typing import List


class Vertex:

    def __init__(self, idx):
        self.idx = idx
        self.out_edges = []

    def __str__(self):
        str_ = f'{{{self.idx}, ('
        for v, _ in self.out_edges:
            str_ += f'{v.idx}, '
        if self.out_edges:
            str_ = str_[:-2]
        return str_ + ')}'


def init_network(network_lines):

    def add_edge(network: List[Vertex], frm_id, to_id, weight):
        frm = network[frm_id]
        to = network[to_id]
        frm.out_edges.append((to, weight))

    v_no, e_no = network_lines[0].split(' ')
    v_no, e_no = int(v_no), int(e_no)
    network = [Vertex(idx) for idx in range(v_no)]
    for line in network_lines[1:]:
        frm_id, to_id, weight = line.split(' ')
        add_edge(network, int(frm_id) - 1, int(to_id) - 1, float(weight))
    return network


def init_seed_set(seed_lines, network):
    seed_set = set()
    for line in seed_lines:
        seed_set.add(network[int(line) - 1])
    return seed_set
