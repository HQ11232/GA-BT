from abc import abstractmethod


class BehaviorTreeAgent(object):
    """Backbone of BT agent.
    An instance which interacts with Environment.
    Embed with two other instances: ConditionChecker and BehaviorTree
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def setup(self):
        """setup elements (if any)"""
        pass

    @abstractmethod
    def reset(self):
        """reset elements (if any)"""
        pass

    @abstractmethod
    def blackboard(self):
        """shortcut to BehaviorTree's blackboard instance"""
        pass

    @abstractmethod
    def tick(self, state):
        """return action given env state
        Flow of information follow these steps:
        argument:
            Env(outside)      --EnvState-->    Agent
        update_condition_checker:
            Agent             --EnvState-->    ConditionChecker
        update_blackboard:
            ConditionChecker  --CondState-->   Blackboard (inside BehaviorTree)
        BehaviorTree.tick:
            Blackboard        --BoardState-->  BehaviorTree
            BehaviorTree      --Action-->      Blackboard
        get_action:
            Blackboard        --Action-->      Agent
        return:
            Agent             --Action-->      Env(outside)
        """
        pass

    @abstractmethod
    def update_condition_checker(self, state):
        """Agent --EnvState--> ConditionChecker"""
        pass

    @abstractmethod
    def update_blackboard(self):
        """ConditionChecker --CondState--> Blackboard"""
        pass

    @abstractmethod
    def get_action(self):
        """Blackboard --Action--> Agent"""
        pass

    @abstractmethod
    def display_blackboard(self):
        """print blackboard variables"""
        pass

    @abstractmethod
    def display_tree(self):
        """print tree structure in ascii fashion"""
        pass
