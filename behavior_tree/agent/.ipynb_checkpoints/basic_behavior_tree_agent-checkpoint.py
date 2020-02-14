from behavior_tree.agent import BehaviorTreeAgent
from behavior_tree.tree import BasicBehaviorTree
from behavior_tree.condition_checker import BasicConditionChecker
from config import *


class BasicBehaviorTreeAgent(BehaviorTreeAgent):
    """Behavior Tree agent with simple hand-crafted rules"""
    def __init__(self, condition_checker=None):
        self.condition_checker = BasicConditionChecker()
        self.tree = BasicBehaviorTree()
    
    def setup(self):
        self.tree.setup()
        return
    
    def reset():
        pass
    
    def tick(self, state):
        # update ConditionChecker state
        self.condition_checker.update_state(state)
        # update blackboard
        self.update_blackboard()
        # tick behavior tree
        self.tree.tick()
        # get action index
        act_idx = self._get_action_idx()
        return act_idx
    
    def update_blackboard(self):
        """write conditions onto blackboard"""
        self.blackboard.condition.CanAccelerate = self.condition_checker.can_accelerate()
        self.blackboard.condition.CanSwitchLeft = self.condition_checker.can_switch_left()
        self.blackboard.condition.CanSwitchRight = self.condition_checker.can_switch_right()
        return
    
    def _get_action(self):
        return self.blackboard.action
    
    def _get_action_idx(self):
        return ACT_TO_ACTIDX[self._get_action()]
    
    @property
    def blackboard(self):
        return self.tree.root.blackboard
