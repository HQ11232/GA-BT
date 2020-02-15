import py_trees
from behavior_tree.agent  import BehaviorTreeAgent
from behavior_tree.tree import GeneticProgrammingBehaviorTree
from behavior_tree.condition_checker import GeneticProgrammingConditionChecker
from config import *


class GeneticProgrammingBehaviorTreeAgent(BehaviorTreeAgent):
    """Genetic-Porgramming-enabled Behavior Tree agent"""
    def __init__(self):
        self.condition_checker = GeneticProgrammingConditionChecker()
        self.tree = GeneticProgrammingBehaviorTree()
        
    def setup(self):
        self.tree.setup()
        return
    
    def reset(self):
        raise NotImplementedError
    
    def tick(self):
        raise NotImplementedError
        
    def update_condition_checker(self, state):
        self.condition_checker.update_state(state)
        return
        
    def update_blackboard(self):
        """update conditions on blackboard"""
        # agent's speed
        self.blackboard.speed = self.condition_checker.speed()
        # free_cells condition
        free_cells = self.condition_checker.free_cells()
        for index, free in enumerate(free_cells):
            self.blackboard.cell_condition[str(index)] = free
        return

    def append_learned_behavior(self, behavior_node):
        """append new behavior with a higher priority"""
        self.tree.root.insert(0, behavior_node)
        return
    
    def display_blackboard(self):
        print(self.blackboard)
        return
    
    def display_tree(self):
        print(py_trees.display.ascii_tree(self.tree.root))
        return
    
    def _get_action(self):
        return self.blackboard.action
    
    def _get_action_idx(self):
        return ACT_TO_ACTIDX[self._get_action()]

    @property
    def blackboard(self):
        return self.tree.root.blackboard