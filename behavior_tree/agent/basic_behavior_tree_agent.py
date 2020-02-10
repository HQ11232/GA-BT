from behavior_tree.agent import BehaviorTreeAgent


class BasicBehaviorTreeAgent(BehaviorTreeAgent):
    """Behavior Tree agent with simple hand-crafted rules"""
    def __init__(self):
        pass
        #self.tree = self._create_tree()
    
    def select_action(self):
        pass
        #return self.blackboard.action
    
    def tick(self):
        pass
    
    @property
    def blackboard(self):
        pass