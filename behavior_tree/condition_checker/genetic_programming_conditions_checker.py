from behavior_tree.conditions_checker import BasicConditionChecker
from config import *


class GeneticProgrammingConditionChecker(BasicConditionChecker):
    """Conditions checker for GP-BT agent"""
    def __init__(self):
        super().__init__()
        
    def free_cells(self):
        """One-dimension list represents free cells"""
        width = self.state.shape[0]
        length = self.state.shape[1]
        cells = [False] * (width * length)
        
        for cell_x in range(width):
            for cell_y in range(length):
                if self.free_in_cell(cell_x, cell_y):
                    cells[(cell_x * length) + cell_y] = True
        return cells
