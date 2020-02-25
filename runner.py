import json
import matplotlib.pyplot as plt
import numpy as np
import py_trees
import sys
import time
import torch
from config import *
from utils import visualize


def play_episode(e, agent, steps=PLAY_EPISODE_STEPS, agent_type='GP-BT',
                 reset=True, debug=False, verbose=False,
                 sleep_time=PLAY_EPISODE_SLEEP_TIME,
                 change_act_sleep_time=CHANGE_ACT_SLEEP_TIME):
    """play one episode, return average speed"""  
    if debug:
        py_trees.logging.level = py_trees.logging.Level.DEBUG
    
    # initilize
    if reset:
        state = e.reset()
        prev_action = ACT_NOACTION
    else:
        state = e._render_state(e.state)
        
    if verbose:
        print("Step: 0")
        visualize(e, full=FULL_VISUALIZE)

    speed_hist = []
    for step in range(steps):
        # append speed
        speed_hist.append(e.current_speed())

        # tick
        if agent_type == 'BT' or agent_type == 'GP-BT':
            action = agent.tick(state[0])
            act_idx = ACT_TO_ACTIDX[action]
        elif agent_type == 'DQN':
            state_v = torch.tensor([state])
            q_v = agent(state_v)[0]
            act_idx = torch.argmax(q_v).item()
            action = ACTIDX_TO_ACT[act_idx]
        else:
            raise ValueError("agent type not specified")
        
        # step
        state, reward, _, _ = e.step(act_idx)
        
        if verbose:
            print("Step:", step+1)
            if (action != prev_action):
                print("action change: {} -> {}".format(prev_action, action))
                prev_action = action
                time.sleep(change_act_sleep_time)
            print(action, e.current_speed(), e.state.my_car.cell_x)
            print('Reward:', reward)
            visualize(e, full=FULL_VISUALIZE)
            print('*' * 50 + '\n')
            time.sleep(sleep_time)
            sys.stdout.flush()
    
    return np.mean(speed_hist)


def measure_performance(e, agent, episodes=PERFORMANCE_TEST_EPISODES, steps=PLAY_EPISODE_STEPS,
                        agent_type='GP-BT', save=False):
    """run for multiple episodes, return avg and std of episodic mean speed"""
    mean_speed = []
    for episode in range(episodes):
        mean_speed.append(play_episode(e, agent, steps=steps, agent_type=agent_type, verbose=False, debug=False))

    performance = {
        'mean_speed': mean_speed,
        'average_mean_speed': np.mean(mean_speed),
        'std_mean_speed': np.std(mean_speed)
    }
   
    plt.hist(mean_speed)
    plt.xlabel("mph")
    plt.title("Histogram of Episodic mean speed: %s %d episodes" %(agent_type, PERFORMANCE_TEST_EPISODES))
    
    if save:
        plt.savefig(SAVEPATH + "hist_%s_%d" %(agent_type, PERFORMANCE_TEST_EPISODES))
        with open(SAVEPATH + "performance__%s_%d.json" %(agent_type, PERFORMANCE_TEST_EPISODES), 'w') as f:
            json.dump(performance, f)
    
    return performance
