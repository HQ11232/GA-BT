from abc import abstractmethod, abstractproperty


class BehaviorTreeAgent:
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def setup(self):
        pass
    
    @abstractmethod
    def reset(self):
        pass
    
    @abstractmethod
    def tick(self):
        pass
    
    @abstractproperty
    def blackboard(self):
        pass
