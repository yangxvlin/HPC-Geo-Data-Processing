"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-11 11:40:01
Description: class to store collected information for grids
"""

from Grid import Grid
from TwitterData import TwitterData


class GridSummary:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.count = 0

    def summarize(self, data: TwitterData):
        y, x = data.location
        if self.grid.is_in_grid(x, y):
            self.count += 1
        return self

    def __repr__(self):
        return "{}: {}".format(self.grid.id, self.count)
