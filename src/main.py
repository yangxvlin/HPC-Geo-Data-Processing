"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-10 15:28:34
Description: 
"""

import mpi4py.MPI as MPI
import numpy as np
import argparse
from pprint import pprint
import json
from collections import Counter


def process_data(location_info, grids_info, count_map):
    """
    :param location_info: {'coordinates': [-34.92320424, 138.59870907], 'type': 'Point'}
    :param grids_info:  [{'id': 'A1', 'xmax': 144.85, 'xmin': 144.7, 'ymax': -37.5, 'ymin': -37.65}, ...]
    :param count_map: {'id': int}
    :return:
    """
    for grid_info in grids_info:
        y, x = location_info["coordinates"]
        if is_in_grid(grid_info["xmax"], grid_info["xmin"], grid_info["ymax"], grid_info["ymin"], x, y):
            count_map[grid_info["id"]] += 1
            return count_map
    return count_map


def main(grid_data_path, geo_data_path):
    # read grid info
    grids = None
    with open(grid_data_path, encoding='utf-8') as file:
        read_data = json.load(file)
        grids = [feature["properties"] for feature in read_data["features"]]

    # initialize communicator
    comm = MPI.COMM_WORLD
    comm_rank = comm.Get_rank()
    comm_size = comm.Get_size()
    # print(comm_rank, comm_size)

    positions = None
    split_positions = None
    # reads data in root process
    if comm_rank == 0:
        with open(geo_data_path, encoding='utf-8') as file:
            read_data = json.load(file)
            positions = [message["json"]["geo"] for message in read_data]
            split_positions = np.array_split(positions, comm_size)

    # divide data to be processed to available processors
    local_data = comm.scatter(split_positions, root=0)

    # pprint(positions)
    # pprint(grids)

    # initialize count map for current_process
    count_map = {i["id"]: 0 for i in grids}

    # process given data
    for position in local_data:
        count_map = process_data(position, grids, count_map)

    # merge count_map
    merged_count_map = comm.reduce(count_map, root=0, op=merge_dicts)

    # output summary in root process
    if comm_rank == 0:
        print(Counter(merged_count_map).most_common())


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
