import py_trees
from behavior_tree.agent  import BehaviorTreeAgent
from behavior_tree.tree import GeneticProgrammingBehaviorTree, ConditionSequenceNode, IntersectConditionSequenceNode
from behavior_tree.condition_checker import GeneticProgrammingConditionChecker
from config import *


class GeneticProgrammingBehaviorTreeAgent(BehaviorTreeAgent):
    """Genetic-Porgramming-enabled Behavior Tree agent"""
    def __init__(self):
        self.condition_checker = GeneticProgrammingConditionChecker()
        self.tree = GeneticProgrammingBehaviorTree()
        self.situation_cnt = 0
        self.behaviour_cnt = 0
        
    def setup(self):
        self.tree.setup()
        return
    
    def reset(self):
        raise NotImplementedError
    
    def tick(self, state):
        # update ConditionChecker state
        self.update_condition_checker(state)
        # update blackboard
        self.update_blackboard()
        # tick behavior tree
        self.tree.tick()
        # get action index
        action = self.get_action()
        return action
        
    def update_condition_checker(self, state):
        self.condition_checker.update_state(state)
        return
        
    def update_blackboard(self):
        """update conditions on blackboard"""
        # agent's speed
        self.blackboard.speed = self.condition_checker.speed()
        # avaialable actions
#         self.blackboard.available_actions[ACT_ACCELERATE] = self.condition_checker.can_accelerate()
#         self.blackboard.available_actions[ACT_DECELERATE] = self.condition_checker.can_decelerate()
#         self.blackboard.available_actions[ACT_SWITCHLEFT] = self.condition_checker.can_switch_left()
#         self.blackboard.available_actions[ACT_SWITCHRIGHT] = self.condition_checker.can_switch_right()
        # free_cells condition
        free_cells = self.condition_checker.free_cells()
        for index, free in enumerate(free_cells):
            self.blackboard.cell_condition[str(index)] = free
        return

    def simplify_situation(self, situation_node, existed_situation_node_name):
        for node_index, learned_behavior_node in enumerate(self.tree.root.children):
            # retrieve CondSeqNode from BehaviorNode
            learned_situation_node = learned_behavior_node.children[0]
            if learned_situation_node.name == existed_situation_node_name:
                new_situation_node = IntersectConditionSequenceNode(situation_node, learned_situation_node)
                # replace existed node
                self.tree.root.children[node_index].children[0] = new_situation_node
                return
        raise ValueError("unable to locate existed situation node during simplification")
            
    
    def append_learned_action(self, situation_node, action_node):
        """append new behavior with a higher priority"""
        behavior_node = py_trees.composites.Sequence(
            name="Behavior{}".format(self.behaviour_cnt),
            children = [situation_node, action_node]
        )
        self.tree.root.children.insert(0, behavior_node)
        self.behaviour_cnt += 1
        return
    
    def display_blackboard(self):
        print(self.blackboard)
        return
    
    def display_tree(self):
        print(py_trees.display.ascii_tree(self.tree.root))
        return
    
    def get_situation(self):
        situation_node = ConditionSequenceNode(self.blackboard.cell_condition, self.situation_cnt)
        self.situation_cnt += 1
        return situation_node
    
    def get_action(self):
        return self.blackboard.action

    @property
    def blackboard(self):
        return self.tree.root.blackboard