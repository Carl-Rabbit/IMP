import random
from typing import List

from model.vertex import Vertex


def get_ic_rrset(vs: List[Vertex], seed: int) -> List:
    active_set = {seed}
    actived = active_set.copy()

    while active_set:
        new_set = set()
        for u_idx in active_set:
            u = vs[u_idx]
            in_degree = len(u.in_edges)
            if in_degree == 0:
                continue
            for v_idx, weight in u.in_edges:
                if v_idx in actived:
                    continue
                if random.random() >= weight:
                    # not active
                    continue
                # active
                actived.add(v_idx)
                new_set.add(v_idx)
        active_set = new_set

    return list(actived)
