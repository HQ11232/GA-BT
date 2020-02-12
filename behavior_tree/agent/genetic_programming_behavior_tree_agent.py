from behavior_tree.agent.basic_behavior_tree_agent import BasicBehaviorTreeAgent
from behavior_tree.tree.genetic_programming_behavior_tree import create_genetic_programming_behavior_tree


class GeneticProgrammingBehaviorTreeAgent(BasicBehaviorTreeAgent):
    """Genetic-Porgramming-enabled Behavior Tree agent"""
    def __init__(self):
        self.condition_checker = condition_checker
        self.tree = create_genetic_programming_behavior_tree(condition_checker)
