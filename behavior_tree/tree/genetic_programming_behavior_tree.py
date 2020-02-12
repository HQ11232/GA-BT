import py_trees


class FreeCellCondition(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super().__init__(name=name)
        self.blackboard = self.attach_blackboard_client(name=self.name)
        self.blackboard.register_key("cell_condition/%s" % (name), access=py_trees.common.Access.READ)
    
    def update(self):
        pass


class TrueFreeCellCondition(FreeCellCondition):
    def __init__(self, name):
        super().__init__(name=name)

    def update(self):
        if self.blackboard.cell_condition[self.name]:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


class FalseFreeCellCondition(FreeCellCondition):
    def __init__(self, name):
        super().__init__(name=name)

    def update(self):
        if self.blackboard.cell_condition[self.name]:
            return py_trees.common.Status.FAILURE
        return py_trees.common.Status.SUCCESS
    

def create_genetic_programming_behavior_tree():
    pass