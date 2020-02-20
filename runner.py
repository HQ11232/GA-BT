import numpy as np
import py_trees
import time
import sys
from config import *
from utils import visualize


def play_episode(e, agent, steps=PLAY_EPISODE_STEPS,
                 reset=True, debug=False, verbose=False,
                 sleep_time=PLAY_EPISODE_SLEEP_TIME,
                 change_act_sleep_time=CHANGE_ACT_SLEEP_TIME):
    """play one episode, return average speed"""  
    # initilize
    if reset:
        state = e.reset()
        agent.setup()
        prev_action = ACT_NOACTION
    else:
        state = e._render_state(e.state)
    
    if debug:
        py_trees.logging.level = py_trees.logging.Level.DEBUG
        
    if verbose:
        print("Step: 0")
        visualize(e, full=False)

    speed_hist = []
    for step in range(steps):
        # append speed
        speed_hist.append(e.current_speed())

        # tick
        action = agent.tick(state[0])
        act_idx = ACT_TO_ACTIDX[action]
        
        # step
        state, reward, _, _ = e.step(act_idx)
        
        if verbose:
            occ = e.state.render_occupancy(full=False)
            print("Step:", step)
            if (action != prev_action):
                print("action change: {} -> {}".format(prev_action, action))
                prev_action = action
                time.sleep(change_act_sleep_time)
            print(action, e.current_speed(), e.state.my_car.cell_x)
            print('Reward:', reward)
            visualize(e, full=False)
            print('*' * 50 + '\n')
            time.sleep(sleep_time)
            sys.stdout.flush()
    
    return np.mean(speed_hist)
