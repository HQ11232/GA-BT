import copy
import logging
import numpy as np
from behavior_tree.tree import ActionSelectorNode
from config import *
from runner import play_episode


def train_GP_BT(e, agent, episodes=TRAIN_EPISODES, steps=PLAY_EPISODE_STEPS):
    # action to situation dict
    action_to_situation_dict = dict() 
    
    for episode in range(episodes):
        # initialize
        logging.info("Episode {}/{}".format(episode+1, episodes))
        state = e.reset()
        agent.setup()
        
        for step in range(steps):
            # enable learning
            agent.blackboard.enable_learning = True
            # tick
            action = agent.tick(state[0])
            
            # learn action invoked
            if action == ACT_LEARN:
                logging.info("step {}/{}: Learn Action triggered".format(step+1, steps))
                # disable learning
                agent.blackboard.enable_learning = False
                # get situation
                situation_node = agent.get_situation()
                
                # learn single action
                action_node = learn_single_action(e, agent, step)
                # switch to GP is no action is learned
                if len(action_node.children) == 0:
                    #action_node = learn_action_using_GP(e, agent, step)
                    logging.info("step {}/{}: no single action found, resort to idle action".format(step+1, steps))
                    act_idx = ACT_TO_ACTIDX[ACT_NOACTION]
                    state, reward, _, _ = e.step(act_idx)
                    continue
                
                # simplify duplicate action
                action_node_key = hash_action_node(action_node)
                if action_node_key in action_to_situation_dict.keys():
                    existed_situation_node_name = action_to_situation_dict[action_node_key]
                    agent.simplify_situation(situation_node, existed_situation_node_name)
                    logging.info("step {}/{}: duplicated action sets, intersect conditions with an existed Behavior".format(step+1, steps))
                else:
                    # add a new learned action
                    agent.append_learned_action(situation_node, action_node)
                    action_to_situation_dict[action_node_key] = situation_node.name
                    logging.info("step {}/{}: new action sets, appended as a new Behavior".format(step+1, steps))
                                  
            # tick without learning
            action = agent.tick(state[0])
            act_idx = ACT_TO_ACTIDX[action]
            state, reward, _, _ = e.step(act_idx)


def train_GP_BT_v2(e, agent, episodes=TRAIN_EPISODES, steps=PLAY_EPISODE_STEPS):
    pass


def learn_single_action(e, agent, steps=TRY_ACTION_STEPS, samples=TRY_ACTION_SAMPLES):
    # sample baseline score (NoAction)
    baseline_score = fitness_score(e, agent, steps=steps, samples=samples)
    
    # total score for each action
    action_score = dict()
    # try each action for multiple episodes
    available_actions = find_available_action(e, agent)
    for action in available_actions:
        score = fitness_score(e, agent, steps=steps, samples=samples, action=action)
        if score > baseline_score:
            action_score[action] = score

    action_list = [key for key, value in sorted(action_score.items(), key=lambda item: item[1], reverse=True)]
    action_node = ActionSelectorNode(action_list)
    return action_node
            

def learn_action_using_GP(e, agent, current_step):
    pass


def hash_action_node(action_node):
    """not yet ready for GP-learned action node"""
    # create key for action node
    key = ''
    for action in action_node.children:
        key += action.name + '_'
    key = key[:-1]  # get rid of the last '_'
    return key


def find_available_action(e, agent):
    state = e._render_state(e.state)[0]
    # update condition checker
    agent.update_condition_checker(state)
    # check for available actions
    available_actions = []
    if agent.condition_checker.can_accelerate():
        available_actions.append(ACT_ACCELERATE)
#     if agent.condition_checker.can_decelerate():
#         available_actions.append(ACT_DECELERATE)
    if agent.condition_checker.can_switch_left():
        available_actions.append(ACT_SWITCHLEFT)
    if agent.condition_checker.can_switch_right():
        available_actions.append(ACT_SWITCHRIGHT)
    return available_actions


def fitness_score(e, agent, steps=TRY_ACTION_STEPS, samples=TRY_ACTION_SAMPLES, action=ACT_NOACTION):
    # initialize
    score = []
    
    # simulation loops
    for sample in range(samples):
        # deep copy env
        e_ = copy.deepcopy(e)
        state = e_._render_state(e_.state)[0]
        # initialize agent
        agent.update_condition_checker(state)
        agent.update_blackboard()
        init_speed = agent.blackboard.speed
        
        # try action
        if action == None:
            action = agent.tick(state)
        state, _, _, _ = e_.step(ACT_TO_ACTIDX[action])
        agent.update_condition_checker(state[0])
        agent.update_blackboard()
        
        # simulate
        _ = play_episode(e_, agent, steps=steps, reset=False)
        
        # score for availability adter T steps
        state = e_._render_state(e_.state)[0]
        agent.update_condition_checker(state)
        agent.update_blackboard()

        avail_score = 0
        can_accelerate = agent.condition_checker.can_accelerate()
        can_switch_left = agent.condition_checker.can_switch_left()
        can_switch_right = agent.condition_checker.can_switch_right()
        if can_accelerate:
            avail_score += CAN_ACCELARATE_SCORE
        elif can_switch_left or can_switch_right:
            avail_score += CAN_SWITCH_LANE
        else:
            pass
        
        # speed score: speed difference
        after_speed = agent.blackboard.speed
        #speed_score = after_speed - init_speed
        speed_score = min(1, max(after_speed - init_speed, -1))
        
        #score.append(speed_score)
        score.append(speed_score + avail_score)
        
    return np.mean(score)
