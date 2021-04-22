import time
import random


def ic_sample(network, seed_set, timestamp_limit):
    active_set = seed_set.copy()
    actived = active_set.copy()
    count = len(active_set)
    while active_set:
        new_set = set()
        for u in active_set:

            # check time
            if time.time() >= timestamp_limit:
                return None

            for v, weight in u.out_edges:
                if v in actived:
                    continue
                rand = random.random()
                if rand > weight:
                    # not active
                    continue
                # active
                actived.add(v)
                new_set.add(v)
        count += len(new_set)
        active_set = new_set

    return count
