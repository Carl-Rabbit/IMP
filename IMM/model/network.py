from model.vertex import Vertex


class Network:

    def __init__(self, network_lines=None):
        self.n = 0
        self.m = 0
        self.vs = []

        if not network_lines:
            return

        self.parse_first_line(network_lines[0])

        for line in network_lines[1:]:
            self.parse_data_line(line)

    def parse_first_line(self, line: str):
        v_no, e_no = line.split(' ')
        self.n, self.m = int(v_no), int(e_no)
        self.vs = [Vertex(idx) for idx in range(self.n)]

    def parse_data_line(self, line: str):
        frm_id, to_id, weight = line.split(' ')
        to = self.vs[int(to_id) - 1]
        edge = (int(frm_id) - 1, float(weight))
        to.in_edges.append(edge)

    def get_est_size(self):
        gesse_size = 24 * self.n + 52 * self.m

        # act_size = sum(sys.getsizeof(v) + sys.getsizeof(v.in_edges) for v in self.vs)
        # print(f'network size: {act_size / 2 ** 20} MB, '
        #       f'gesse_size: {gesse_size / 2 ** 20} MB')

        return gesse_size

