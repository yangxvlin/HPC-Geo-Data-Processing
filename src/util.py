"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-11 11:52:44
Description: some helper functions
"""

import json
from Grid import Grid
from GridSummary import GridSummary


def preprocess_data(data: str):
    """
    :param data:
    :return: data with end ',' truncated otherwise return None
    """
    if data.endswith(',\n'):
        return data[:-2]
    elif data.endswith(','):
        return data[:-1]
    return None


def read_grid_information(file_path: str):
    grids_summary = []

    with open(file_path, encoding='utf-8') as file:
        json_data = json.load(file)
        for grid_info in json_data["features"]:
            grid = Grid(grid_info["properties"])
            grids_summary.append(GridSummary(grid))

    return grids_summary
