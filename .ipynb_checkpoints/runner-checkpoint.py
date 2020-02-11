import numpy as np
import py_trees
import time
import sys
from config import *


def play_episode(e, agent, steps=PLAY_EPISODE_STEPS,
                 debug=False, verbose=False, sleep_time=PLAY_EPISODE_SLEEP_TIME):
    """Play one episode, agent should be linked to environment beforehand"""
    assert agent.condition_checker._env is e, "agent is looking at different env"
    
    # initilize
    _ = e.reset()
    agent.setup()
    speed_hist = []
    
    if debug:
        py_trees.logging.level = py_trees.logging.Level.DEBUG

    for _ in range(steps):
        # append speed
        speed_hist.append(e.current_speed())

        # tick
        agent.tick()
        action = agent.get_action()
        action_num = agent.get_action_num()

        # step
        _, reward, _, _ = e.step(action_num)
        
        if verbose:
            occ = e.state.render_occupancy(full=False)
            print(occ.T)
            print(action, e.state.my_car.safe_speed, e.state.my_car.cell_x)
            print('reward:', reward)
            time.sleep(sleep_time)
            sys.stdout.flush()
    
    return np.mean(speed_hist)
