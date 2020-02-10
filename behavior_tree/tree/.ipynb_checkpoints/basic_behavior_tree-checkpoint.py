import py_trees


class CanAccelerate(py_trees.behaviour.Behaviour):
    """Condition trigger leaf for [acceleration]"""
    def __init__(self):
        super().__init__(name="CanAccelerate")
    
    def update(self):
        return py_trees.common.Status.SUCCESS

    
class CanSwitchLeft(py_trees.behaviour.Behaviour):
    """Condition trigger leaf for [switching to left lane]"""
    def __init__(self):
        super().__init__(name="CanSwitchLeft")
    
    def update(self):
        return py_trees.common.Status.SUCCESS


class CanSwitchRight(py_trees.behaviour.Behaviour):
    """Condition trigger leaf for [switching to right lane]"""
    def __init__(self):
        super().__init__(name='CanSwitchRight')
    
    def update(self):
        return py_trees.common.Status.SUCCESS


class Accelerate(py_trees.behaviour.Behaviour):
    """Behavior leaf for [acceleration]"""
    def __init__(self):
        super().__init__(name="Accelerate")
        
    def update(self):
        return py_trees.common.Status.RUNNING

    
class SwitchLeft(py_trees.behaviour.Behaviour):
    """Behavior leaf for [switching to left lane]"""
    def __init__(self):
        super().__init__(name="SwitchLeft")
        
    def update(self):
        return py_trees.common.Status.RUNNING
    

class SwitchRight(py_trees.behaviour.Behaviour):
    """Behavior leaf for [switching to right lane]"""
    def __init__(self):
        super().__init__(name="SwitchRight")
        
    def update(self):
        return py_trees.common.Status.RUNNING
    

class NoAction(py_trees.behaviour.Behaviour):
    """Default behavior, [no action]"""
    def __init__(self):
        super().__init__(name="NoAction")
    
    def update(self):
        return py_trees.common.Status.RUNNING
    

def create_basic_behavior_tree(name="Planner"):
    """assemble leaves and nodes"""
    root = py_trees.composites.Selector(name=name)
    
    # plan for acceleration
    plan_accelerate = py_trees.composites.Sequence(name="PlanAccelerate")
    can_accelerate = CanAccelerate()
    accelerate = Accelerate()
    plan_accelerate.add_child(can_accelerate)
    plan_accelerate.add_child(accelerate)
    
    # plan for lane switching
    plan_switch = py_trees.composites.Selector(name="PlanSwitch")
    plan_switch_left = py_trees.composites.Sequence(name="PlamSwitchLeft")
    plan_switch_right = py_trees.composites.Sequence(name="PlanSwitchRight")
    can_switch_left = CanSwitchLeft()
    can_switch_right = CanSwitchRight()
    switch_left = SwitchLeft()
    switch_right = SwitchRight()
    plan_switch_left.add_child(can_switch_left)
    plan_switch_left.add_child(switch_left)
    plan_switch_right.add_child(can_switch_right)
    plan_switch_right.add_child(switch_right)
    plan_switch.add_child(plan_switch_left)
    plan_switch.add_child(plan_switch_right)
    
    # idle action
    no_action = NoAction()
    
    # ensemble planners
    root.add_child(plan_accelerate)
    root.add_child(plan_switch)
    root.add_child(no_action)
    
    tree = py_trees.trees.BehaviourTree(root)
    
    return tree
