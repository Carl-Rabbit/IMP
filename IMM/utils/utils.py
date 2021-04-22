import argparse
from typing import List


TEMP_OUTPUT_PATH = 'tmp/tmp.log'


def param_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-k', '--seed_cnt', type=int, default=4)
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()
    file_name = args.file_name
    seed_cnt = args.seed_cnt
    model = args.model
    time_limit = args.time_limit

    return file_name, seed_cnt, model, time_limit


def read_lines(file_name) -> List[str]:
    with open(file_name, 'r') as fp:
        lines = fp.readlines()
    return lines


def write_lines(file_name, lines):
    with open(file_name, 'w', encoding='utf-8') as fp:
        for line in lines:
            fp.write(line + '\n')


def print_tmp(* value, sep=' ', end='\n'):
    with open(TEMP_OUTPUT_PATH, 'a') as fp:
        for v in value:
            fp.write(str(v) + sep)
        fp.write(end)
