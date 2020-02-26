import argparse
import numpy as np
import torch
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from behavior_tree.agent import BasicBehaviorTreeAgent, GeneticProgrammingBehaviorTreeAgent
from config import *
from deep_traffic.libtraffic import env, model
from utils import render_image


def show_demo(e, agent, agent_type='GP-BT'):
    occ = e.state.render_occupancy(full=False).T
    shape = (occ.shape[0] * HEIGHT_SCALE, occ.shape[1] * WIDTH_SCALE)
    
    fig, ax = plt.subplots()
    ax.set_xlim(shape[1])
    ax.set_ylim(shape[0])
    
    def update(frame):
        ln = plt.imshow(frame, interpolation='bilinear')
        return ln,

    ani = FuncAnimation(fig, update, 
                        frames=frame_func(e, agent, agent_type=agent_type), 
                        blit=True, interval=100)
    plt.show()

    
def frame_func(e, agent, agent_type='GP-BT'):
    # initilize
    state = e._render_state(e.state)

    while True:
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
        state, _, _, _ = e.step(act_idx)
        
        yield(render_image(e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", '--model', required=True, help="Agent type: [BT]/[GP-BT]/[DQN]")
    args = parser.parse_args()
    
    # initilize env
    e = env.DeepTraffic(lanes_side=LANES_SIDE, 
                        patches_ahead=PATCHES_AHEAD,
                        patches_behind=PATCHES_BEHIND, 
                        history=HISTORY, 
                        obs=OBS)
    _ = e.reset()
    
    # initilize agent
    if args.model == 'BT':
        agent = BasicBehaviorTreeAgent()
    elif args.model == 'GP-BT':
        agent = GeneticProgrammingBehaviorTreeAgent()
        agent.load()
        agent.blackboard.enable_learning = False
    else:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        agent = model.DQN(e.obs_shape, e.action_space.n)
        agent.load_state_dict(torch.load(DQNMODELPATH, map_location=device))
        print("Pretrained model: %s" %(DQNMODELPATH))
    
    show_demo(e, agent, agent_type=args.model)