from abc import abstractmethod, abstracyproperty


class BehaviorTreeAgent:
    @abstractmethod
    def __init__(self):
        pass

    @abstactmethod
    def select_action(self):
        pass
    
    @abstactmethod
    def tick(self):
        pass
    
    @abstactproperty
    def blackboard(self):
        pass
