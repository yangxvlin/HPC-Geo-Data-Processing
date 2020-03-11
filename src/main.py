"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-10 15:28:34
Description: 
"""

from datetime import datetime
import mpi4py.MPI as MPI
import numpy as np
import argparse
from pprint import pprint
import json
from collections import Counter
from TwitterData import TwitterData
from util import read_grid_information, read_data_line_by_line, preprocess_data


def process_data(data, grids_info, count_map):
    """
    :param data:
    :param grids_info:  [{'id': 'A1', 'xmax': 144.85, 'xmin': 144.7, 'ymax': -37.5, 'ymin': -37.65}, ...]
    :param count_map: {'id': int}
    :return:
    """
    for grid_info in grids_info:
        y, x = data["json"]["geo"]["coordinates"]
        if is_in_grid(grid_info["xmax"], grid_info["xmin"], grid_info["ymax"], grid_info["ymin"], x, y):
            count_map[grid_info["id"]] += 1
            return count_map
    return count_map


def main(grid_data_path, geo_data_path):
    grids_summary = read_grid_information(grid_data_path)

    # initialize communicator
    comm = MPI.COMM_WORLD
    comm_rank = comm.Get_rank()
    comm_size = comm.Get_size()
    # print(comm_rank, comm_size)

    start = datetime.now()

    # only one process, no need to split data
    if comm_size == 1:
        for line in read_data_line_by_line(geo_data_path):
            preprocessed_line = preprocess_data(line)
            # the line is data
            if preprocessed_line:
                twitter_data = TwitterData(preprocessed_line)
                grids_summary = list(map(lambda x: x.summarize(twitter_data), grids_summary))

    # else:
    #     if comm_rank == 0:
    #
    #     else:

    # merge count_map
    # merged_count_map = comm.reduce(count_map, root=0, op=merge_dicts)

    # output summary in root process
    if comm_rank == 0:
        grids_summary = sorted(grids_summary, key=lambda x: x.count, reverse=True)
        pprint(grids_summary)
        end = datetime.now()
        print(f"Programs runs", end - start)


def merge_dicts(x: dict, y: dict):
    """
    :param x:
    :param y:
    :return: merge two dictionaries with common key's values added
    """
    z = Counter(x)
    z.update(Counter(y))
    return z


def is_in_grid(xmax, xmin, ymax, ymin, x, y):
    if xmin <= x <= xmax and ymin <= y <= ymax:
        return True
    return False


if __name__ == "__main__":
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='python to process data')
    # Required grid data path
    parser.add_argument('-grid', type=str, help='A required string path to grid file')
    # Required geo data path
    parser.add_argument('-data', type=str, help='A required string path to geo data file')
    args = parser.parse_args()

    grid = args.grid
    data = args.data

    main(grid, data)
