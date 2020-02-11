from abc import abstractmethod, abstractproperty


class BehaviorTreeAgent:
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_action(self):
        pass
    
    @abstractmethod
    def get_action_num(self):
        pass
    
    @abstractmethod
    def tick(self):
        pass
    
    @abstractmethod
    def setup(self):
        pass
    
    @abstractproperty
    def blackboard(self):
        pass
