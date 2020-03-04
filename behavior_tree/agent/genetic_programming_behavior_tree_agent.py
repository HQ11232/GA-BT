import math

import py_trees

from behavior_tree.agent import BehaviorTreeAgent
from behavior_tree.condition_checker import GeneticProgrammingConditionChecker
from behavior_tree.tree import GeneticProgrammingBehaviorTree, ConditionSequenceNode, \
    CustomNodeByName, IntersectConditionSequenceNode
from config import *


class GeneticProgrammingBehaviorTreeAgent(BehaviorTreeAgent):
    """Genetic-Programming-enabled Behavior Tree agent"""

    def __init__(self):
        super().__init__()
        self.condition_checker = GeneticProgrammingConditionChecker()
        self.tree = GeneticProgrammingBehaviorTree()
        self.situation_cnt = 0  # identifier for SituationNode
        self.behaviour_cnt = 0  # identifier for BehaviourNode

    def setup(self):
        self.tree.setup()
        self.blackboard.available_actions = {}
        self.blackboard.cell_condition = {}
        self.blackboard.enable_learning = False
        return

    def reset(self):
        self.situation_cnt = 0
        self.behaviour_cnt = 0
        return

    @property
    def blackboard(self):
        return self.tree.root.blackboard

    def tick(self, state):
        # update ConditionChecker state
        self.update_condition_checker(state)
        # update blackboard
        self.update_blackboard()
        # tick behavior tree
        self.tree.tick()
        # get action
        action = self.get_action()
        return action

    def update_condition_checker(self, state):
        self.condition_checker.update_state(state)
        return

    def update_blackboard(self):
        # agent's speed
        self.blackboard.speed = self.condition_checker.speed()
        # available_actions
        self.blackboard.available_actions[ACT_ACCELERATE] = self.condition_checker.can_accelerate()
        #self.blackboard.available_actions[ACT_DECELERATE] = self.condition_checker.can_decelerate()
        self.blackboard.available_actions[ACT_SWITCHLEFT] = self.condition_checker.can_switch_left()
        self.blackboard.available_actions[ACT_SWITCHRIGHT] = self.condition_checker.can_switch_right()
        # free cells condition
        free_cells = self.condition_checker.free_cells()
        for index, free in enumerate(free_cells):
            self.blackboard.cell_condition[str(index)] = free
        return

    def get_action(self):
        return self.blackboard.action

    def display_blackboard(self):
        print(self.blackboard)
        return

    def display_tree(self):
        print(py_trees.display.ascii_tree(self.tree.root))
        return

    def get_situation(self):
        """return ConditionSequenceNode from current BoardState"""
        situation_node = ConditionSequenceNode(self.blackboard.cell_condition, self.situation_cnt)
        self.situation_cnt += 1
        return situation_node

    def get_change_situation(self, cell_condition_old: dict):
        """return ConditionSequenceNode from parts of current BoardState which differ from given BoardState"""
        cell_condition = self.blackboard.cell_condition
        change_cell_condition = dict()
        # iterate over current states
        for key, value in cell_condition.items():
            # pick up only states that changes
            if value != cell_condition_old[key]:
                change_cell_condition[key] = value
        change_situation_node = ConditionSequenceNode(change_cell_condition, self.situation_cnt)
        self.situation_cnt += 1
        return change_situation_node

    def simplify_situation(self, situation_node: ConditionSequenceNode, existed_situation_node_name: str):
        """merge a new ConditionSequenceNode with an existed one given node's name"""
        # iterate over root's children
        for node_index, learned_behavior_node in enumerate(self.tree.root.children):
            # extract ConditionSequenceNode from BehaviorNode
            learned_situation_node = learned_behavior_node.children[0]
            # check if node's name matches
            if learned_situation_node.name == existed_situation_node_name:
                # create a new merged CSNode
                new_situation_node = IntersectConditionSequenceNode(situation_node, learned_situation_node)
                # replace the existed node
                self.tree.root.children[node_index].children[0] = new_situation_node
                return
        raise ValueError("unable to locate existed situation node during simplification")

    def append_learned_action(self, situation_node: ConditionSequenceNode, action_node: py_trees.composites.Selector):
        """append a new BehaviorNode to the tree with the highest priority
        BehaviorNode = Sequence(SituationNode, ActionNode)
        """
        behavior_node = py_trees.composites.Sequence(
            name="Behavior%d" % self.behaviour_cnt,
            children=[situation_node, action_node]
        )
        self.tree.root.children.insert(0, behavior_node)  # highest priority
        self.behaviour_cnt += 1
        return

    def save(self, name='GP-BT'):
        """save tree structure as .tree file"""
        with open(BTMODELPATH + name + '.tree', 'w') as f:
            f.write(py_trees.display.ascii_tree(self.tree.root))
            print("Save model at %s" % (BTMODELPATH + name + '.tree'))
        return

    def load(self, name='GP-BT'):
        try:
            with open(BTMODELPATH + name + '.tree', 'r') as f:
                lines = f.read()
            print("Load model from %s" % (BTMODELPATH + name + '.tree'))
        except FileNotFoundError:
            print("File not found. Resort to default initialization.")
            return

        # reconstruct tree
        root = py_trees.composites.Selector(name='root')
        frontier = {0: root}  # depth: last node
        for line in lines.split('\n')[1:]:
            # skip blank line
            if len(line) == 0:
                continue
            # extract information
            depth = math.floor(line.count(' ') / 4)
            name = line.split()[-1]
            # add new node
            try:
                new_node = CustomNodeByName(name)
            except ValueError:
                continue
            frontier[depth - 1].add_child(new_node)
            # update
            frontier[depth] = new_node

        # reconstruct blackboard
        root.blackboard = root.attach_blackboard_client(name="root")
        root.blackboard.register_key("action", access=py_trees.common.Access.READ)
        root.blackboard.register_key("speed", access=py_trees.common.Access.WRITE)
        root.blackboard.register_key("available_actions", access=py_trees.common.Access.WRITE)
        root.blackboard.register_key("enable_learning", access=py_trees.common.Access.WRITE)
        root.blackboard.register_key("cell_condition", access=py_trees.common.Access.WRITE)

        self.tree = py_trees.trees.BehaviourTree(root)
        return
