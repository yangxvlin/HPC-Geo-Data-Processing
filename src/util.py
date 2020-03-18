"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-11 11:52:44
Description: some helper functions
"""

import json
from Language import Language


def preprocess_data(data: str):
    """
    :param data:
    :return: data with end ',' truncated otherwise return None
    """
    if data.endswith('},\n'):
        return data[:-2]
    elif data.endswith('}\n'):
        return data[:-1]
    print("invalid line:", data)
    return None


# def read_grid_information(file_path: str):
#     grids_summary_dict = {}
#
#     with open(file_path, encoding='utf-8') as file:
#         json_data = json.load(file)
#         for grid_info in json_data["features"]:
#             grid = Grid(grid_info["properties"])
#             grids_summary_dict[grid.id] = GridSummary(grid)
#
#     return grids_summary_dict


def read_language_code(file_path: str):
    language_dict = {}

    with open(file_path, encoding='utf-8') as file:
        json_data = json.load(file)
        for language_code in json_data:
            language = Language(language_code, json_data[language_code])
            language_dict[language_code] = language

    return language_dict


def read_data_line_by_line(file_path: str):
    with open(file_path, encoding='utf-8') as file:
        for line in file:
            yield line

