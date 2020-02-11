import py_trees
from deep_traffic.libtraffic import env
from behavior_tree.agent.basic_behavior_tree_agent import BasicBehaviorTreeAgent
from behavior_tree.conditions_checker import BasicConditionChecker
from behavior_tree.tree.basic_behavior_tree import create_basic_behavior_tree
from runner import play_episode
from config import *


def main():
    # initilize env
    e = env.DeepTraffic(lanes_side=LANES_SIDE, patches_ahead=PATCHES_AHEAD,
                        patches_behind=PATCHES_BEHIND, history=HISTORY, obs=OBS)
    _ = e.reset()
    
    # initilize condition checker
    condition_checker = BasicConditionChecker(e)
    
    # initilize agent
    agent = BasicBehaviorTreeAgent(condition_checker)
    
    # play episode
    mean_speed = play_episode(e, agent, verbose=True, debug=False, sleep_time=0.5)
    print('Mean Speed:', mean_speed)


if __name__ == '__main__':
    main()
