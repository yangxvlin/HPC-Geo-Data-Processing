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


def main(grid_data_path, geo_data_path):
    # read grid info
    grids = None
    with open(grid_data_path) as file:
        read_data = json.load(file)
        grids = [feature["properties"] for feature in read_data["features"]]

    pprint(grids)


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
