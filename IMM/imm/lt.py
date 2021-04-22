import random
from typing import List

from model.vertex import Vertex


def get_lt_rrset(vs: List[Vertex], seed: int) -> List:
    actived = {seed}
    cur = vs[seed]
    while cur.in_edges:
        in_degree = len(cur.in_edges)
        r = int(random.random() * in_degree)
        v_idx, _ = cur.in_edges[r]
        if v_idx in actived:
            break
        cur = vs[v_idx]
        actived.add(v_idx)
    return list(actived)
