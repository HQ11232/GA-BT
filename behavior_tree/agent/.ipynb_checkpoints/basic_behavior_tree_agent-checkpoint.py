from behavior_tree.agent.behavior_tree_agent import BehaviorTreeAgent
from behavior_tree.tree.basic_behavior_tree import create_basic_behavior_tree


class BasicBehaviorTreeAgent(BehaviorTreeAgent):
    """Behavior Tree agent with simple hand-crafted rules"""
    def __init__(self, condition_checker=None):
        self.condition_checker = condition_checker
        self.tree = create_basic_behavior_tree(condition_checker)
    
    def get_action(self):
        return self.blackboard.action
    
    def get_action_num(self):
        return self.blackboard.action_num
    
    def tick(self):
        self.tree.tick()
        return
    
    def setup(self):
        self.tree.setup()
        return
    
    @property
    def blackboard(self):
        return self.tree.root.blackboard
