import py_trees


class CanAccelerate(py_trees.behaviour.Behaviour):
    """Condition trigger leaf for [acceleration]"""
    def __init__(self, condition_checker):
        super().__init__(name="CanAccelerate")
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("condition/CanAccelerate", access=py_trees.common.Access.WRITE)
        self.condition_checker = condition_checker
    
    def update(self):
        if self.condition_checker.can_accelerate():
            self.blackboard.condition.CanAccelerate = True
            return py_trees.common.Status.SUCCESS
        self.blackboard.condition.CanAccelerate = False
        return py_trees.common.Status.FAILURE

    
class CanSwitchLeft(py_trees.behaviour.Behaviour):
    """Condition trigger leaf for [switching to left lane]"""
    def __init__(self, condition_checker):
        super().__init__(name="CanSwitchLeft")
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("condition/CanSwitchLeft", access=py_trees.common.Access.WRITE)
        self.condition_checker = condition_checker
    
    def update(self):
        if self.condition_checker.can_switch_left():
            self.blackboard.condition.CanSwitchLeft = True
            return py_trees.common.Status.SUCCESS
        self.blackboard.condition.CanSwitchLeft = False
        return py_trees.common.Status.FAILURE


class CanSwitchRight(py_trees.behaviour.Behaviour):
    """Condition trigger leaf for [switching to right lane]"""
    def __init__(self, condition_checker):
        super().__init__(name='CanSwitchRight')
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("condition/CanSwitchRight", access=py_trees.common.Access.WRITE)
        self.condition_checker = condition_checker
    
    def update(self):
        if self.condition_checker.can_switch_right():
            self.blackboard.condition.CanSwitchRight = True
            return py_trees.common.Status.SUCCESS
        self.blackboard.condition.CanSwitchRight = False
        return py_trees.common.Status.FAILURE


class Accelerate(py_trees.behaviour.Behaviour):
    """Behavior leaf for [acceleration]"""
    def __init__(self):
        super().__init__(name="Accelerate")
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("condition/CanAccelerate", access=py_trees.common.Access.READ)
        self.blackboard.register_key("action", access=py_trees.common.Access.WRITE)
        self.blackboard.register_key("action_num", access=py_trees.common.Access.WRITE)
        
    def update(self):
        if not self.blackboard.condition.CanAccelerate:
            return py_trees.common.Status.FAILURE
        self.blackboard.action = "accelerate"
        self.blackboard.action_num = 1
        return py_trees.common.Status.SUCCESS

    
class SwitchLeft(py_trees.behaviour.Behaviour):
    """Behavior leaf for [switching to left lane]"""
    def __init__(self):
        super().__init__(name="SwitchLeft")
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("condition/CanSwitchLeft", access=py_trees.common.Access.READ)
        self.blackboard.register_key("action", access=py_trees.common.Access.WRITE)
        self.blackboard.register_key("action_num", access=py_trees.common.Access.WRITE)
        
    def update(self):
        if not self.blackboard.condition.CanSwitchLeft:
            return py_trees.common.Status.FAILURE
        self.blackboard.action = "goLeft"
        self.blackboard.action_num = 3
        return py_trees.common.Status.SUCCESS
    

class SwitchRight(py_trees.behaviour.Behaviour):
    """Behavior leaf for [switching to right lane]"""
    def __init__(self):
        super().__init__(name="SwitchRight")
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("condition/CanSwitchRight", access=py_trees.common.Access.READ)
        self.blackboard.register_key("action", access=py_trees.common.Access.WRITE)
        self.blackboard.register_key("action_num", access=py_trees.common.Access.WRITE)
        
    def update(self):
        if not self.blackboard.condition.CanSwitchRight:
            return py_trees.common.Status.FAILURE
        self.blackboard.action = "goRight"
        self.blackboard.action_num = 4
        return py_trees.common.Status.SUCCESS
    

class NoAction(py_trees.behaviour.Behaviour):
    """Default behavior, [no action]"""
    def __init__(self):
        super().__init__(name="NoAction")
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("condition/CanAccelerate", access=py_trees.common.Access.READ)
        self.blackboard.register_key("condition/CanSwitchLeft", access=py_trees.common.Access.READ)
        self.blackboard.register_key("condition/CanSwitchRight", access=py_trees.common.Access.READ)
        self.blackboard.register_key("action", access=py_trees.common.Access.WRITE)
        self.blackboard.register_key("action_num", access=py_trees.common.Access.WRITE)
    
    def update(self):
        if (self.blackboard.condition.CanAccelerate\
            or self.blackboard.condition.CanSwitchLeft\
            or self.blackboard.condition.CanSwitchRight):
            return py_trees.common.Status.FAILURE
        self.blackboard.action = "noAction"
        self.blackboard.action_num = 0
        return py_trees.common.Status.SUCCESS
    

def create_basic_behavior_tree(condition_checker, name="Planner"):
    """assemble leaves and nodes"""
    root = py_trees.composites.Selector(name=name)
    
    # plan for acceleration
    plan_accelerate = py_trees.composites.Sequence(name="PlanAccelerate")
    can_accelerate = CanAccelerate(condition_checker)
    accelerate = Accelerate()
    plan_accelerate.add_child(can_accelerate)
    plan_accelerate.add_child(accelerate)
    
    # plan for lane switching
    plan_switch = py_trees.composites.Selector(name="PlanSwitch")
    plan_switch_left = py_trees.composites.Sequence(name="PlamSwitchLeft")
    plan_switch_right = py_trees.composites.Sequence(name="PlanSwitchRight")
    can_switch_left = CanSwitchLeft(condition_checker)
    can_switch_right = CanSwitchRight(condition_checker)
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
    
    # add blackboard for reading action
    root.blackboard = root.attach_blackboard_client(name=name)
    root.blackboard.register_key("action", access=py_trees.common.Access.READ)
    root.blackboard.register_key("action_num", access=py_trees.common.Access.READ)
    
    tree = py_trees.trees.BehaviourTree(root)
    
    return tree
