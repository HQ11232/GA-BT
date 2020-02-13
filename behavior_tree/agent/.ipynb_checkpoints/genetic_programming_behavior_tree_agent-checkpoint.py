from behavior_tree.agent.basic_behavior_tree_agent import BasicBehaviorTreeAgent
from behavior_tree.tree.genetic_programming_behavior_tree import create_genetic_programming_behavior_tree


class GeneticProgrammingBehaviorTreeAgent(BasicBehaviorTreeAgent):
    """Genetic-Porgramming-enabled Behavior Tree agent"""
    def __init__(self, condition_checker=None):
        self.condition_checker = condition_checker
        self.tree = create_genetic_programming_behavior_tree()
        
    def write_state_conditions_on_blackboard(self):
        """agent access tree's blackboard and write free cell conditions"""
        free_cells = self.condition_checker.free_cells()
        for index, free in enumerate(free_cells):
            self.blackboard.cell_condition[str(index)] = free
        return

    def append_learned_behavior(self, behavior_node):
        """append new behavior with a higher priority"""
        self.tree.root.insert(0, behavior_node)
        return