from behavior_tree.agent import BehaviorTreeAgent
from behavior_tree.tree import BasicBehaviorTree
from behavior_tree.condition_checker import BasicConditionChecker
from config import *


class BasicBehaviorTreeAgent(BehaviorTreeAgent):
    """Behavior Tree agent with simple hand-crafted rules"""
    def __init__(self):
        self.condition_checker = BasicConditionChecker()
        self.tree = BasicBehaviorTree()
    
    def setup(self):
        self.tree.setup()
        return
    
    def reset(self):
        raise NotImplementedError
    
    def tick(self, state):
        # update ConditionChecker state
        self.condition_checker.update_state(state)
        # update blackboard
        self.update_blackboard()
        # tick behavior tree
        self.tree.tick()
        # get action index
        action = self.get_action()
        return action
    
    def update_blackboard(self):
        """write conditions onto blackboard"""
        self.blackboard.condition.CanAccelerate = self.condition_checker.can_accelerate()
        self.blackboard.condition.CanSwitchLeft = self.condition_checker.can_switch_left()
        self.blackboard.condition.CanSwitchRight = self.condition_checker.can_switch_right()
        return
    
    def display_blackboard(self):
        print(self.blackboard)
        return
    
    def display_tree(self):
        print(py_trees.display.ascii_tree(self.tree.root))
        return
    
    def get_action(self):
        return self.blackboard.action
    
    @property
    def blackboard(self):
        return self.tree.root.blackboard
