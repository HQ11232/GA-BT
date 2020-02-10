class ConditionChecker:
    """Class for check conditions which trigger BT leaf nodes"""
    
    def __init__(self, env):
        self._env = env
        self.car_length = env.state.my_car.Length
        self.safety_front = env.state.Safety_front
        self.switch_lane_safety_front = env.state.Safety_front + 2
        self.cell_x = self._env.lanes_side
        self.cell_y = self._env.patches_ahead
    
    @property
    def state(self):
        """Perception field of current timestep"""
        return self._env._render_state(self._env.state)[0]
    
    def can_accelerate(self):
        """Conditions lead to acceleration action"""
        # no car in safety front range
        if self.car_in_front():
            return False
        return True
    
    def can_switch_left(self):
        """Conditions lead to switching to left lane"""
        # not in the leftmost lane
        if self.in_leftmost_lane():
            return False
        if self.car_at_left():
            return False
        return True
    
    def can_switch_right(self):
        """Conditions lead to switching to right lane"""
        # not in the rightmost lane
        if self.in_rihgtmost_lane():
            return False
        if self.cat_at_right():
            return False
        return True

    def car_in_front(self):
        """Any car in safety front range"""
        if self.car_in_range(self.cell_x, self.cell_y - self.safety_front - 1, self.cell_y - 1):
            return True
        return False
    
    def car_at_left(self):
        """Any car to the left, including safety range"""
        if self.car_in_range(self.cell_x - 1, self.cell_y - self.switch_lane_safety_front - 1, self.cell_y - 1):
            return True
        if self.car_in_range(self.cell_x - 1, self.cell_y + self.car_length, self.cell_y + self.car_length + self.safety_front/2):
            return True
        return False
    
    def car_at_right(self):
        """Any car to the right, including safety range"""
        if self.car_in_range(self.cell_x + 1, self.cell_y - self.switch_lane_safety_front - 1, self.cell_y - 1):
            return True
        if self.car_in_range(self.cell_x + 1, self.cell_y + self.car_length, self.cell_y + self.car_length + self.safety_front/2):
            return False
    
    def car_in_cell(self, cell_x, cell_y):
        if self.state[cell_x, cell_y] != 1:
            return True
        return False
    
    def car_in_range(self, cell_x, cell_y_min, cell_y_max):
        if any ([
            self.car_in_cell(cell_x, y) 
            for y in range(cell_y_min, cell_y_max + 1)
        ]):
            return True
        return False
    
    def in_leftmost_lane(self):
        if self.state[self.cell_x - 1, self.cell_y] == 0:
            return True
        return False
    
    def in_rightmost_lane(self):
        if self.state[self.cell_x + 1, self.cell_y] == 0:
            return True
        return False
