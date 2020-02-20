from config import *

class ConditionChecker(object):
    """Class for check conditions which trigger BT leaf nodes"""
    def __init__(self):
        self.car_length = 4  # from deepTraffic setting
        self.safety_front = SAFETY_FRONT
        self.switch_lane_safety_front = SWITCH_LANE_SAFETY_FRONT
        self.cell_x = LANES_SIDE
        self.cell_y = PATCHES_AHEAD
        self.state = None
        
    def update_state(self, state):
        self.state = state
