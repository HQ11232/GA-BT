import py_trees

from config import *


class SafetyCondition(py_trees.behaviour.Behaviour):
    """ConditionNode for SafetyNode"""

    def __init__(self, name='SafetyCond'):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("speed", access=py_trees.common.Access.READ)

    def update(self):
        """trigger safety action when speed is too low"""
        if self.blackboard.speed <= MIN_SAFETY_SPEED:
            return py_trees.common.Status.FAILURE
        return py_trees.common.Status.SUCCESS


class SafetyAct(py_trees.behaviour.Behaviour):
    """ActionNode for SafetyNode"""

    def __init__(self, name='SafetyAct'):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("action", access=py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.action = SAFETY_ACTION
        return py_trees.common.Status.SUCCESS


class LearnAct(py_trees.behaviour.Behaviour):
    """LearnActNode, when activated triggers ACT_LEARN"""

    def __init__(self, name='LearnAct'):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("enable_learning", access=py_trees.common.Access.READ)
        self.blackboard.register_key("action", access=py_trees.common.Access.WRITE)

    def update(self):
        if self.blackboard.enable_learning:
            self.blackboard.action = ACT_LEARN
            return py_trees.common.Status.SUCCESS
        self.blackboard.action = ACT_NOACTION
        return py_trees.common.Status.FAILURE


def SafetyNode(name='SafetyNode'):
    """SafetyNode = Selector(SafetyCondition, SafetyAct)"""
    node = py_trees.composites.Selector(name=name)
    node.add_child(SafetyCondition(name='SafetyCond'))
    node.add_child(SafetyAct(name='SafetyAct'))
    return node


def InitialRoot(name='InitialRoot'):
    """InitialRoot = Selector(SafetyNode, LearnNode)"""
    init_root = py_trees.composites.Sequence(name=name)
    init_root.add_child(SafetyNode())
    init_root.add_child(LearnAct(name))
    return init_root


class FreeCellCondition(py_trees.behaviour.Behaviour):
    """Backbone for FreeCellCondition leaf"""

    def __init__(self, name):
        super().__init__(name=name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("cell_condition", access=py_trees.common.Access.READ)

    def update(self):
        pass


class TrueFreeCellCondition(FreeCellCondition):
    """TrueFreeCellCondition, activates when corresponding cell is free"""

    def __init__(self, name):
        super().__init__(name='T' + name)

    def update(self):
        if self.blackboard.cell_condition[self.name[1:]]:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


class FalseFreeCellCondition(FreeCellCondition):
    """TrueFreeCellCondition, activates when corresponding cell is not free"""

    def __init__(self, name):
        super().__init__(name='F' + name)

    def update(self):
        if self.blackboard.cell_condition[self.name[1:]]:
            return py_trees.common.Status.FAILURE
        return py_trees.common.Status.SUCCESS


def ConditionSequenceNode(free_cell_conditions, cond_index):
    """SequenceNode of FreeCellConditionNodes according to current free cell conditions"""
    assert isinstance(free_cell_conditions, dict), "free cell conditions should be accessed via blackboard"
    conditions_sequence = py_trees.composites.Sequence(name="Cond{}".format(cond_index))
    for cell_index, free_cell in free_cell_conditions.items():
        if free_cell:
            conditions_sequence.add_child(TrueFreeCellCondition(name=str(cell_index)))
        else:
            conditions_sequence.add_child(FalseFreeCellCondition(name=str(cell_index)))
    return conditions_sequence


def IntersectConditionSequenceNode(new_node, existed_node):
    """SequenceNode contains intersection of FreeCellConditions of two ConditionSequenceNodes"""
    # get all condition names of the new node
    new_cond_names = set([child.name for child in new_node.children])
    # create new list for only non-intersected child
    new_children = [child for child in existed_node.children if child.name in new_cond_names]
    # replace existed children with a new set
    existed_node.children = new_children
    return existed_node


class CustomActionNode(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("available_actions", access=py_trees.common.Access.READ)
        self.blackboard.register_key("action", access=py_trees.common.Access.WRITE)

    def update(self):
        # activate only if available
        if self.blackboard.available_actions[self.name]:
            self.blackboard.action = self.name
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


def ActionSelectorNode(action_list):
    """ActionSelectorNode = Selector(CustomActionNode_1, ... , CustomActionNode_N)"""
    action_selector = py_trees.composites.Selector()
    if len(action_list) == 0:
        return action_selector
    for action in action_list:
        action_selector.add_child(CustomActionNode(name=action))
    return action_selector


def CustomNodeByName(name):
    """return corresponding node given name"""
    if 'T' in name:
        return TrueFreeCellCondition(name=name[1:])
    elif 'F' in name:
        return FalseFreeCellCondition(name=name[1:])
    elif 'Cond' in name \
            or 'Behavior' in name:
        return py_trees.composites.Sequence(name=name)
    elif 'Selector' in name:
        return py_trees.composites.Selector(name=name)
    elif ACT_ACCELERATE in name \
            or ACT_DECELERATE in name \
            or ACT_SWITCHLEFT in name \
            or ACT_SWITCHRIGHT in name:
        return CustomActionNode(name=name)
    elif 'InitRoot' in name:
        return InitialRoot()
    else:
        raise ValueError("node name is unknown: %s" % name)


def GeneticProgrammingBehaviorTree() -> py_trees.trees.BehaviourTree:
    """Initial Tree setup of GP-BT"""
    # create initial root
    init_root = InitialRoot()
    # add a selector above initial root to keep blackboard in-place
    root = py_trees.composites.Selector(name="root")
    root.add_child(init_root)
    # attach blackboard
    root.blackboard = root.attach_blackboard_client(name="root")
    root.blackboard.register_key("action", access=py_trees.common.Access.READ)
    root.blackboard.register_key("speed", access=py_trees.common.Access.WRITE)
    root.blackboard.register_key("available_actions", access=py_trees.common.Access.WRITE)
    root.blackboard.register_key("enable_learning", access=py_trees.common.Access.WRITE)
    root.blackboard.register_key("cell_condition", access=py_trees.common.Access.WRITE)

    tree = py_trees.trees.BehaviourTree(root)
    return tree
