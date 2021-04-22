from typing import List


def read_lines(file_name) -> List[str]:
    with open(file_name, 'r') as fp:
        lines = fp.readlines()
    return lines
