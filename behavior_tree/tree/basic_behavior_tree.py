import py_trees
from config import *


class CanAccelerate(py_trees.behaviour.Behaviour):
    """Condition trigger leaf for [acceleration]"""
    def __init__(self, name="CanAccelerate"):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("condition/CanAccelerate", access=py_trees.common.Access.READ)
    
    def update(self):
        if self.blackboard.condition.CanAccelerate:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE

    
class CanSwitchLeft(py_trees.behaviour.Behaviour):
    """Condition trigger leaf for [switching to left lane]"""
    def __init__(self, name="CanSwitchLeft"):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("condition/CanSwitchLeft", access=py_trees.common.Access.READ)

    def update(self):
        if self.blackboard.condition.CanSwitchLeft:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


class CanSwitchRight(py_trees.behaviour.Behaviour):
    """Condition trigger leaf for [switching to right lane]"""
    def __init__(self, name='CanSwitchRight'):
        super().__init__(name='CanSwitchRight')
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("condition/CanSwitchRight", access=py_trees.common.Access.READ)
    
    def update(self):
        if self.blackboard.condition.CanSwitchRight:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


class Accelerate(py_trees.behaviour.Behaviour):
    """Behavior leaf for [acceleration]"""
    def __init__(self, name="Accelerate"):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("action", access=py_trees.common.Access.WRITE)
        
    def update(self):
        self.blackboard.action = ACT_ACCELERATE
        return py_trees.common.Status.SUCCESS

    
class SwitchLeft(py_trees.behaviour.Behaviour):
    """Behavior leaf for [switching to left lane]"""
    def __init__(self, name="SwitchLeft"):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("action", access=py_trees.common.Access.WRITE)
        
    def update(self):
        self.blackboard.action = ACT_SWITCHLEFT
        return py_trees.common.Status.SUCCESS
    

class SwitchRight(py_trees.behaviour.Behaviour):
    """Behavior leaf for [switching to right lane]"""
    def __init__(self, name="SwitchRight"):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("action", access=py_trees.common.Access.WRITE)
        
    def update(self):
        self.blackboard.action = ACT_SWITCHRIGHT
        return py_trees.common.Status.SUCCESS
    

class NoAction(py_trees.behaviour.Behaviour):
    """Default behavior, [no action]"""
    def __init__(self, name="NoAction"):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("action", access=py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.action = ACT_NOACTION
        return py_trees.common.Status.SUCCESS
    

def BasicBehaviorTree(name="Planner"):
    """assemble leaves and nodes"""
    root = py_trees.composites.Selector(name=name)
    
    # plan for acceleration
    plan_accelerate = py_trees.composites.Sequence(name="PlanAccelerate")
    can_accelerate = CanAccelerate(name="CanAccelerate")
    accelerate = Accelerate(name="Accelerate")
    plan_accelerate.add_child(can_accelerate)
    plan_accelerate.add_child(accelerate)
    
    # plan for lane switching
    plan_switch = py_trees.composites.Selector(name="PlanSwitch")
    plan_switch_left = py_trees.composites.Sequence(name="PlamSwitchLeft")
    plan_switch_right = py_trees.composites.Sequence(name="PlanSwitchRight")
    can_switch_left = CanSwitchLeft(name="CanSwitchLeft")
    can_switch_right = CanSwitchRight(name="CanSwitchRight")
    switch_left = SwitchLeft(name="SwitchLeft")
    switch_right = SwitchRight(name="SwitchRight")
    plan_switch_left.add_child(can_switch_left)
    plan_switch_left.add_child(switch_left)
    plan_switch_right.add_child(can_switch_right)
    plan_switch_right.add_child(switch_right)
    plan_switch.add_child(plan_switch_left)
    plan_switch.add_child(plan_switch_right)
    
    # idle action
    no_action = NoAction(name="NoAction")
    
    # ensemble planners
    root.add_child(plan_accelerate)
    root.add_child(plan_switch)
    root.add_child(no_action)
    
    # add blackboard for reading action
    root.blackboard = root.attach_blackboard_client(name=name)
    root.blackboard.register_key("action", access=py_trees.common.Access.READ)
    root.blackboard.register_key("condition/CanAccelerate", access=py_trees.common.Access.WRITE)
    root.blackboard.register_key("condition/CanSwitchLeft", access=py_trees.common.Access.WRITE)
    root.blackboard.register_key("condition/CanSwitchRight", access=py_trees.common.Access.WRITE)
    
    tree = py_trees.trees.BehaviourTree(root)
    return tree
