import numpy as np
import py_trees
import time
import sys
from config import *
from utils import visualize


def play_episode(e, agent, steps=PLAY_EPISODE_STEPS,
                 debug=False, verbose=False, interactive=False,
                 sleep_time=PLAY_EPISODE_SLEEP_TIME,
                 change_act_sleep_time=CHANGE_ACT_SLEEP_TIME):
    """play one episode, return average speed"""  
    # initilize
    agent.setup()
    state = e.reset()
    speed_hist = []
    prev_action = ACT_NOACTION
    
    if debug:
        py_trees.logging.level = py_trees.logging.Level.DEBUG  
    
    if verbose:
        print("Step: 0")
        visualize(e, full=False)

    for step in range(steps):
        # append speed
        speed_hist.append(e.current_speed())

        # tick
        act_idx = agent.tick(state[0])
        action = agent._get_action()
        
        # step
        state, reward, _, _ = e.step(act_idx)
        
        if verbose:
            occ = e.state.render_occupancy(full=False)
            print("Step:", step)
            if (action != prev_action):
                print("action change: {} -> {}".format(prev_action, action))
                prev_action = action
                time.sleep(change_act_sleep_time)
            print(action, e.state.my_car.safe_speed, e.state.my_car.cell_x)
            print('Reward:', reward)
            visualize(e, full=False)
            print('*' * 50 + '\n')
            time.sleep(sleep_time)
            sys.stdout.flush()
    
    return np.mean(speed_hist)


def train_gp():
    pass
