"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-11 11:15:26
Description: class to contain grid information
"""


class Grid:
    def __init__(self, grid: dict):
        self.id = grid["id"]
        self.xmin = grid["xmin"]
        self.xmax = grid["xmax"]
        self.ymin = grid["ymin"]
        self.ymax = grid["ymax"]

    def is_in_grid(self, x, y):
        if self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax:
            return True
        return False

    def __hash__(self):
        return hash(self.id)
