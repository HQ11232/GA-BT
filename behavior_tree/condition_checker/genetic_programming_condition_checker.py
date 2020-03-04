from abc import ABC

from behavior_tree.condition_checker import BasicConditionChecker
from config import *


class GeneticProgrammingConditionChecker(BasicConditionChecker, ABC):
    """Conditions checker for GP-BT agent"""

    def __init__(self):
        super().__init__()

    def speed(self):
        """state: real speed of an agent (mph)"""
        return round(self.state[self.cell_x, self.cell_y] * SPEED_FACTOR)

    def free_cells(self):
        """state: one-dimension list represents of free cells"""
        width = self.state.shape[0]
        length = self.state.shape[1]
        cells = [False] * (width * length)
        # iterate over all cells
        for cell_x in range(width):
            for cell_y in range(length):
                if self.free_in_cell(cell_x, cell_y):
                    cells[(cell_x * length) + cell_y] = True
        return cells

    def free_in_cell(self, cell_x, cell_y):
        """condition: no car and not outside of the road"""
        if (self.state[cell_x, cell_y] != 1) and (self.state[cell_x, cell_y] != 0):
            return True
        return False
