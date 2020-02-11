class ConditionChecker:
    """Class for check conditions which trigger BT leaf nodes"""
    def __init__(self, env):
        self._env = env
        self.car_length = int(env.state.my_car.Length)
        self.safety_front = int(env.state.Safety_front)
        self.cell_x = int(self._env.lanes_side)
        self.cell_y = int(self._env.patches_ahead)
    
    @property
    def state(self):
        """Perception field of current timestep"""
        return self._env._render_state(self._env.state)[0]
