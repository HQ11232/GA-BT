import argparse

import torch

from behavior_tree.agent import BasicBehaviorTreeAgent, GeneticProgrammingBehaviorTreeAgent
from config import *
from deep_traffic.libtraffic import env, model
from runner import play_episode, measure_performance


def main(args):
    # initialize env
    e = env.DeepTraffic(lanes_side=LANES_SIDE,
                        patches_ahead=PATCHES_AHEAD,
                        patches_behind=PATCHES_BEHIND,
                        history=HISTORY,
                        obs=OBS)
    e.reset()

    # initialize agent
    if args.model == 'BT':
        agent = BasicBehaviorTreeAgent()
        agent.setup()
    elif args.model == 'GP-BT':
        agent = GeneticProgrammingBehaviorTreeAgent()
        agent.load(name='GP-BT_v%d' % args.version)
        agent.setup()
    elif args.model == 'DQN':
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        agent = model.DQN(e.obs_shape, e.action_space.n)
        agent.load_state_dict(torch.load(DQNMODELPATH, map_location=device))
        print("Pre-trained model: %s" % DQNMODELPATH)
    else:
        raise ValueError("specified unknown model: %s" % args.model)

    # play episode
    mean_speed = play_episode(e, agent, agent_type=args.model, verbose=args.verbose)
    print('Mean Speed: %.2f mph' % mean_speed)

    # measure performance by playing multiple episodes
    performance = measure_performance(e, agent, agent_type=args.model, steps=PERFORMANCE_TEST_EPISODES, save=True)
    print('Average Episodic mean speed: %.2f mph' % performance['average_mean_speed'])
    print('STD Episodic mean speed: %.2f mph' % performance['std_mean_speed'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", '--model', required=True, help="Agent type: [BT]/[GP-BT]/[DQN]")
    parser.add_argument("--version", type=int, default=1, help="version for GP-BT, specify [1, 2, 3]")
    parser.add_argument("--verbose", action='store_true', help="Display individual steps")
    args = parser.parse_args()

    main(args)
