from typing import List


class Vertex:

    def __init__(self, idx):
        self.idx = idx
        self.in_edges: List[tuple] = []

    def __repr__(self):
        str_ = f'{{{self.idx}, ('
        for edge in self.in_edges:
            str_ += f'{edge}, '
        if self.in_edges:
            str_ = str_[:-2]
        return str_ + ')}'
