"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-11 11:15:26
Description: class to contain grid information
"""


class Grid:
    def __init__(self, grid: dict):
        self.id = grid["features"]["properties"]["id"]
        self.xmin = grid["features"]["properties"]["xmin"]
        self.xmax = grid["features"]["properties"]["xmax"]
        self.ymin = grid["features"]["properties"]["ymin"]
        self.ymax = grid["features"]["properties"]["ymax"]

    def is_in_grid(self, x, y):
        if self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax:
            return True
        return False

    def __hash__(self):
        return hash(self.id)
