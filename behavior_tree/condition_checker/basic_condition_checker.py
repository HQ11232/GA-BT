from behavior_tree.condition_checker import ConditionChecker


class BasicConditionChecker(ConditionChecker):
    """ConditionChecker for BasicBehaviorTreeAgent"""

    def __init__(self):
        super().__init__()

    def can_accelerate(self):
        """conditions lead to ACT_ACCELERATE"""
        # no car in safety front range
        if self.car_in_front():
            return False
        return True

    def can_decelerate(self):
        """conditions lead to ACT_DECELERATE"""
        raise NotImplementedError

    def can_switch_left(self):
        """conditions lead to ACT_SWITCHLEFT"""
        # not in the leftmost lane
        if self.in_leftmost_lane():
            return False
        # no car in the left
        if self.car_at_left():
            return False
        return True

    def can_switch_right(self):
        """conditions lead to ACT_SWITCHRIGHT"""
        # not in the rightmost lane
        if self.in_rightmost_lane():
            return False
        # no car in the right
        if self.car_at_right():
            return False
        return True

    def car_in_front(self):
        """condition: any car in safety front range"""
        if self.car_in_range(self.cell_x, self.cell_y - self.safety_front - 1, self.cell_y - 1):
            return True
        return False

    def car_at_left(self):
        """condition: any car to the left (including safety range)"""
        if self.car_in_range(self.cell_x - 1,
                             self.cell_y - self.switch_lane_safety_front - 1,
                             self.cell_y + self.car_length):
            return True
        return False

    def car_at_right(self):
        """condition: any car to the right (including safety range)"""
        if self.car_in_range(self.cell_x + 1,
                             self.cell_y - self.switch_lane_safety_front - 1,
                             self.cell_y + self.car_length):
            return True
        return False

    def car_in_cell(self, cell_x, cell_y):
        """condition: any car in given cell"""
        if self.state[cell_x, cell_y] != 1:
            return True
        return False

    def car_in_range(self, cell_x, cell_y_min, cell_y_max):
        """condition: any car in given range"""
        if any([
            self.car_in_cell(cell_x, y)
            for y in range(cell_y_min, cell_y_max + 1)
        ]):
            return True
        return False

    def in_leftmost_lane(self):
        """condition: exist in the leftmost lane"""
        if self.state[self.cell_x - 1, self.cell_y] == 0:
            return True
        return False

    def in_rightmost_lane(self):
        """condition: exist in the rightmost lane"""
        if self.state[self.cell_x + 1, self.cell_y] == 0:
            return True
        return False
