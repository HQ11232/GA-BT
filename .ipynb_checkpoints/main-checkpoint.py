import argparse
import torch
from deep_traffic.libtraffic import env, model
from behavior_tree.agent import BasicBehaviorTreeAgent
from runner import play_episode
from config import *


def main(args):
    # initilize env
    e = env.DeepTraffic(lanes_side=LANES_SIDE, 
                        patches_ahead=PATCHES_AHEAD,
                        patches_behind=PATCHES_BEHIND, 
                        history=HISTORY, 
                        obs=OBS)
    
    # initilize agent
    if args.model == 'BT':
        agent = BasicBehaviorTreeAgent()
    elif args.model == 'GP-BT':
        agent = BasicBehaviorTreeAgent()
    else:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        agent = model.DQN(e.obs_shape, e.action_space.n)
        agent.load_state_dict(torch.load(MODELPATH, map_location=device))
    
    # play episode
    mean_speed = play_episode(e, agent, agent_type=args.model, verbose=args.verbose, debug=args.debug)
    print('Mean Speed:', mean_speed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", '--model', required=True, help="Agent type: [BT]/[GP-BT]/[DQN]")
    parser.add_argument("-v", "--verbose", action='store_true', help="Display individual steps")
    parser.add_argument("-d", "--debug", action='store_true', help="Display BT debugger")
    args = parser.parse_args()

    main(args)