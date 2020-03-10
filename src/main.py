"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-10 15:28:34
Description: 
"""

from mpi4py import *
import numpy as np
import argparse
from pprint import pprint
import json
from collections import defaultdict


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

    # reads data
    positions = None
    with open(geo_data_path, encoding='utf-8') as file:
        read_data = json.load(file)
        positions = [message["json"]["geo"] for message in read_data]

    pprint(positions)
    # pprint(grids)

    count_map = defaultdict(lambda: 0)
    # process positions data
    for position in positions:
        count_map = process_data(position, grids, count_map)

    # output summary
    print(count_map)


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
