import py_trees
from config import *


class FreeCellCondition(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super().__init__(name=name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("cell_condition", access=py_trees.common.Access.READ)
    
    def update(self):
        pass


class TrueFreeCellCondition(FreeCellCondition):
    def __init__(self, name):
        super().__init__(name='T'+name)

    def update(self):
        if self.blackboard.cell_condition[self.name[1:]]:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


class FalseFreeCellCondition(FreeCellCondition):
    def __init__(self, name):
        super().__init__(name='F'+name)

    def update(self):
        if self.blackboard.cell_condition[self.name[1:]]:
            return py_trees.common.Status.FAILURE
        return py_trees.common.Status.SUCCESS


class SafetyCondition(py_trees.behaviour.Behaviour):
    """Condition node for SafetyNode"""
    def __init__(self, name):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("speed", access=py_trees.common.Access.READ)
        
    def update(self):
        """trigger safety act when speed is very low"""
        if self.blackboard.speed <= MIN_SAFETY_SPEED:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE
        

class SafetyAct(py_trees.behaviour.Behaviour):
    """ActionNode for SafetyNode"""
    def __init__(self, name):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("action", access=py_trees.common.Access.WRITE)
        
    def update(self):
        self.blackboard.action = SAFETY_ACTION
        return py_trees.common.Status.SUCCESS


class LearnAct(py_trees.behaviour.Behaviour):
    """LearnNode, when activate write 'Learn Action' onto blackboard"""
    def __init__(self, name):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("action", access=py_trees.common.Access.WRITE)
        
    def update(self):
        if ENABLE_LEARNING:
            self.blackboard.action = 'LearnAction'
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


def create_safety_node():
    """SafetyNode composes of Safety Condition and Safety Act leaves"""
    node = py_trees.composites.Sequence(name="SafetyNode")
    node.add_child(SafetyCondition(name='SafetyCond'))
    node.add_child(SafetyAct(name='SafetyAct'))
    return node


def create_initial_root():
    """Initial root includes a Sequence of SafetyNode and LearnNode"""
    init_root = py_trees.composites.Sequence(name="InitRoot")
    init_root.add_child(create_safety_node())
    init_root.add_child(LearnAct(name='LearnAct'))
    return init_root


def create_condition_sequence(free_cell_conditions, cond_index):
    """Create SequenceNode of FreeCellConditionNodes according to current free cell conditions"""
    conditions_sequence = py_trees.composites.Sequence(name="Cond{}".format(cond_index))
    for cell_index, free_cell in free_cell_conditions.items():
        if free_cell:
            conditions_sequence.add_child(TrueFreeCellCondition(name=str(cell_index)))
        else:
            conditions_sequence.add_child(FalseFreeCellCondition(name=str(cell_index)))
    
    return conditions_sequence
    
    
def create_genetic_programming_behavior_tree():
    # create initial root
    init_root = create_initial_root()
    
    # add a selector above initial root (to keep blackboard in-place)
    root = py_trees.composites.Selector(name="root")
    root.add_child(init_root)
    
    # blackboard
    root.blackboard = root.attach_blackboard_client(name="root")
    root.blackboard.register_key("action", access=py_trees.common.Access.READ)
    root.blackboard.register_key("speed", access=py_trees.common.Access.WRITE)
    root.blackboard.register_key("cell_condition", access=py_trees.common.Access.WRITE)
    root.blackboard.cell_condition = {}
    
    tree = py_trees.trees.BehaviourTree(root)
    
    return tree
    