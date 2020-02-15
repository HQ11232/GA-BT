from deep_traffic.libtraffic import env
from behavior_tree.agent import BasicBehaviorTreeAgent
from behavior_tree.condition_checker import BasicConditionChecker
from behavior_tree.tree import BasicBehaviorTree
from runner import play_episode
from config import *


def main():
    # initilize env
    e = env.DeepTraffic(lanes_side=LANES_SIDE, 
                        patches_ahead=PATCHES_AHEAD,
                        patches_behind=PATCHES_BEHIND, 
                        history=HISTORY, 
                        obs=OBS)
    
    # initilize agent
    agent = BasicBehaviorTreeAgent()
    
    # play episode
    mean_speed = play_episode(e, agent, verbose=True, debug=False, sleep_time=0.25)
    print('Mean Speed:', mean_speed)


if __name__ == '__main__':
    main()
