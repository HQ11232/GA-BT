from behavior_tree.agent  import BehaviorTreeAgent
from behavior_tree.tree import GeneticProgrammingBehaviorTree
from behavior_tree.condition_checker import GeneticProgrammingConditionChecker
from config import *


class GeneticProgrammingBehaviorTreeAgent(BehaviorTreeAgent):
    """Genetic-Porgramming-enabled Behavior Tree agent"""
    def __init__(self):
        self.condition_checker = GeneticProgrammingConditionChecker
        self.tree = GeneticProgrammingBehaviorTree
        
    def setup(self):
        self.tree.setup()
        return
    
    def reset(self):
        pass
    
    def tick(self):
        pass
        
    def update_blackboard(self):
        """agent access tree's blackboard and write free cell conditions"""
        free_cells = self.condition_checker.free_cells()
        for index, free in enumerate(free_cells):
            self.blackboard.cell_condition[str(index)] = free
        return

    def append_learned_behavior(self, behavior_node):
        """append new behavior with a higher priority"""
        self.tree.root.insert(0, behavior_node)
        return

    @property
    def blackboard(self):
        return self.tree.root.blackboard