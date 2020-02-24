import argparse
import torch
from behavior_tree.agent import BasicBehaviorTreeAgent, GeneticProgrammingBehaviorTreeAgent
from config import *
from deep_traffic.libtraffic import env, model
from runner import play_episode, measure_performance


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
        print("Pretrained model: %s" %(MODELPATH))
    
    # play episode
    mean_speed = play_episode(e, agent, agent_type=args.model, verbose=args.verbose, debug=args.debug)
    print('Mean Speed: %.2f mph' %(mean_speed))
    
    # measure performace by playing multiple episodes
    performance = measure_performance(e, agent, agent_type=args.model, steps=PERFORMANCE_TEST_EPISODES, save=True)
    print('Average Episodic mean speed: %.2f mph' %(performance['average_mean_speed']))
    print('STD Episodic mean speed: %.2f mph' %(performance['std_mean_speed']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", '--model', required=True, help="Agent type: [BT]/[GP-BT]/[DQN]")
    parser.add_argument("-v", "--verbose", action='store_true', help="Display individual steps")
    parser.add_argument("-d", "--debug", action='store_true', help="Display BT debugger")
    args = parser.parse_args()

    main(args)
