import copy
from config import *
from runner import play_episode


def train_GP_BT(e, agent, episodes=100, steps=200):
    # action to situation dict
    action_to_situation_dict = dict() 
    
    for episode in range(episodes):
        # initialize
        state = e.reset()
        agent.setup()
        
        for step in range(steps):
            # tick
            action = agent.tick(state[0])
            
            # apply action
            if action == ACT_LEARN:
                # get situation
                situation_node = agent.get_situation()
                
                # learn single action
                action_node = learn_single_action(e, agent, step)
                # switch to GP is no action is learned
                if len(action.children) == 0:
                    action_node = learn_action_using_GP(e, agent, step)
                
                # simplify duplicate action
                action_node_key = hash_action_node(action_node)
                if action_node_key in action_to_situation_dict.keys():
                    existed_situation_node_name = action_to_situation_dict[action_node_key]
                    agent.simplify_situation(situation_node, existed_situation_node_name)
                else:
                    # add a new learned action
                    agent.append_learned_action(situation_node, action_node)
                    action_to_situation_dict[action_node_key] = situation_node.name
                
            else:
                act_idx = ACT_TO_ACTIDX[action]
                state, reward, _, _ = e.step(act_idx)
                

def learn_single_action(e, agent, current_step, samples=30):
    # total score for each action
    action_score = dict()
    
    # try each action for multiple episodes
    for action in ACT_TO_ACTIDX:
        act_score = 0
        for sample in samples:
            # deep copy agent and env
            e_ = copy.deepcopy(e)
            agent_ = copy.deepcopy(agent)
            
            # try action
            state, _, _, _ = e_.step(ACT_TO_ACTIDX[action])
            
            # simulate, calculate score in Monte-Carlo fashion
            mean_speed = play_episode(e, agent, steps=PLAY_EPISODE_STEPS - current_step, reset=False, init_state=state)
            act_score += mean_speed
        act_score /= samples
        action_score[action] = act_score
    pass
            


def learn_action_using_GP(e, agent, current_step):
    pass


def hash_action_node(action_node):
    """not yet ready for GP-learned action node"""
    # create key for action node
    key = ''
    for action in action_node.children():
        key += action.name + '_'
    key = key[:-1]  # get rid of the last '_'
    return key
