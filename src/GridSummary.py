"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-11 11:40:01
Description: class to store collected information for grids
"""

from Grid import Grid


class GridSummary:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.count = 0

    def summarize(self, data: dict):
        y, x = data["json"]["geo"]["coordinates"]
        if self.grid.is_in_grid(x, y):
            self.count += 1
