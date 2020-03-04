import argparse
import copy
import logging

import numpy as np

from behavior_tree.agent import GeneticProgrammingBehaviorTreeAgent
from behavior_tree.tree import ActionSelectorNode
from config import *
from deep_traffic.libtraffic import env
from runner import play_episode

logging.basicConfig(level=logging.INFO)


def train_GP_BT(e, agent,
                episodes=TRAIN_EPISODES, steps=PLAY_EPISODE_STEPS):
    """training algorithm implemented in textbook"""
    # action to situation dict
    action_to_situation_dict = dict()

    for episode in range(episodes):
        # initialize
        logging.info("Episode {}/{}".format(episode + 1, episodes))
        state = e.reset()
        agent.setup()

        for step in range(steps):
            # enable learning
            agent.blackboard.enable_learning = True
            # tick
            action = agent.tick(state[0])

            # learn action invoked
            if action == ACT_LEARN:
                logging.info("Episode {}/{} Step {}/{}: Learn Action triggered"
                             .format(episode + 1, episodes, step + 1, steps))
                # disable learning
                agent.blackboard.enable_learning = False
                # get situation
                situation_node = agent.get_situation()
                # learn single action
                action_node = learn_single_action(e, agent)
                # switch to GP is no action is learned
                if len(action_node.children) == 0:
                    # action_node = learn_action_using_GP(e, agent)
                    logging.info("Episode {}/{} Step {}/{}: no single action found, resort to idle action"
                                 .format(episode + 1, episodes, step + 1, steps))
                    act_idx = ACT_TO_ACTIDX[ACT_NOACTION]
                    state, reward, _, _ = e.step(act_idx)
                    continue
                # simplify duplicate action
                action_node_key = hash_action_node(action_node)
                if action_node_key in action_to_situation_dict.keys():
                    existed_situation_node_name = action_to_situation_dict[action_node_key]
                    agent.simplify_situation(situation_node, existed_situation_node_name)
                    logging.info("Episode {}/{} Step {}/{}: duplicated action sets,"
                                 " intersect conditions with an existed Behavior"
                                 .format(episode + 1, episodes, step + 1, steps))
                # add a new learned action
                else:
                    agent.append_learned_action(situation_node, action_node)
                    action_to_situation_dict[action_node_key] = situation_node.name
                    logging.info("Episode {}/{} Step {}/{}: new action sets, appended as a new Behavior"
                                 .format(episode + 1, episodes, step + 1, steps))

            # tick again
            action = agent.tick(state[0])
            act_idx = ACT_TO_ACTIDX[action]
            state, reward, _, _ = e.step(act_idx)

    return


def train_GP_BT_v2(e, agent, episodes=TRAIN_EPISODES, steps=PLAY_EPISODE_STEPS):
    """training algorithm implemented in MARIO PAPER"""
    for episode in range(episodes):
        # initialize
        logging.info("Episode {}/{}".format(episode + 1, episodes))
        state = e.reset()
        agent.setup()
        # initial fitness and condition
        r_old = fitness_score_v2(e, agent)
        cell_condition_old = copy.deepcopy(agent.blackboard.cell_condition)
        logging.info("Episode {}/{}: Initial Fitness {}".format(episode + 1, episodes, r_old))

        for step in range(steps):
            # get current fitness and condition
            r = fitness_score_v2(e, agent)
            cell_condition = copy.deepcopy(agent.blackboard.cell_condition)
            logging.info("Episode {}/{} Step {}/{}: Fitness {}"
                         .format(episode + 1, episodes, step + 1, steps, r))

            # learn new action if fitness does not increase
            if (r < 1) and (r <= r_old) and (cell_condition != cell_condition_old):
                logging.info("Episode {}/{} Step {}/{}: Learn Action triggered"
                             .format(episode + 1, episodes, step + 1, steps))
                # get change situation
                change_situation_node = agent.get_change_situation(cell_condition_old)
                # learn single action
                action_node = learn_single_action(e, agent)
                # switch to GP is no action is learned
                if len(action_node.children) == 0:
                    # action_node = learn_action_using_GP(e, agent)
                    logging.info("Episode {}/{} Step {}/{}: no single action found, resort to idle action"
                                 .format(episode + 1, episodes, step + 1, steps))
                    act_idx = ACT_TO_ACTIDX[ACT_NOACTION]
                    state, reward, _, _ = e.step(act_idx)
                    continue
                # add a new learned action
                agent.append_learned_action(change_situation_node, action_node)
                logging.info("Episode {}/{} Step {}/{}: appended a new Behavior"
                             .format(episode + 1, episodes, step + 1, steps))
                # update condition and fitness
                cell_condition_old = cell_condition
                r_old = r

            # tick again
            action = agent.tick(state[0])
            act_idx = ACT_TO_ACTIDX[action]
            state, reward, _, _ = e.step(act_idx)

    return


def train_GP_BT_v3(e, agent, episodes=TRAIN_EPISODES, steps=PLAY_EPISODE_STEPS):
    """custom algorithm combines v1 and v2"""
    # action to situation dict
    action_to_situation_dict = dict()

    for episode in range(episodes):
        # initialize
        logging.info("Episode {}/{}".format(episode + 1, episodes))
        state = e.reset()
        agent.setup()
        # initial fitness and condition
        r_old = fitness_score_v2(e, agent)
        logging.info("Episode {}/{}: Initial Fitness {}".format(episode + 1, episodes, r_old))

        for step in range(steps):
            # get current fitness and condition
            r = fitness_score_v2(e, agent)
            logging.info("Episode {}/{} Step {}/{}: Fitness {}".format(episode + 1, episodes, step + 1, steps, r))

            # learn new action if fitness does not increase
            if (r < 1) and (r <= r_old):
                logging.info("Episode {}/{} Step {}/{}: Learn Action triggered"
                             .format(episode + 1, episodes, step + 1, steps))
                # get situation
                situation_node = agent.get_situation()
                # learn single action
                action_node = learn_single_action(e, agent)
                # switch to GP is no action is learned
                if len(action_node.children) == 0:
                    # action_node = learn_action_using_GP(e, agent)
                    logging.info("Episode {}/{} Step {}/{}: no single action found, resort to idle action"
                                 .format(episode + 1, episodes, step + 1, steps))
                    act_idx = ACT_TO_ACTIDX[ACT_NOACTION]
                    state, reward, _, _ = e.step(act_idx)
                    continue
                # simplify duplicate action
                action_node_key = hash_action_node(action_node)
                if action_node_key in action_to_situation_dict.keys():
                    existed_situation_node_name = action_to_situation_dict[action_node_key]
                    agent.simplify_situation(situation_node, existed_situation_node_name)
                    logging.info("Episode {}/{} Step {}/{}: duplicated action sets, "
                                 "intersect conditions with an existed Behavior"
                                 .format(episode + 1, episodes, step + 1, steps))
                # add a new learned action
                else:
                    agent.append_learned_action(situation_node, action_node)
                    action_to_situation_dict[action_node_key] = situation_node.name
                    logging.info("Episode {}/{} Step {}/{}: new action sets, appended as a new Behavior"
                                 .format(episode + 1, episodes, step + 1, steps))

            # tick again
            action = agent.tick(state[0])
            act_idx = ACT_TO_ACTIDX[action]
            state, reward, _, _ = e.step(act_idx)
            # update fitness
            r_old = r

    return


def learn_single_action(e, agent,
                        steps=TRY_ACTION_STEPS, samples=TRY_ACTION_SAMPLES):
    """return ActionSelectorNode of single actions that score higher than baseline"""
    # sample baseline score (NoAction)
    baseline_score = fitness_score(e, agent, steps=steps, samples=samples)
    # total score for each action
    action_score = dict()
    available_actions = find_available_action(e, agent)
    for action in available_actions:
        score = fitness_score(e, agent, steps=steps, samples=samples, action=action)
        # only add action better than baseline
        if score > baseline_score:
            action_score[action] = score
    # return ActionSelectorNode, sorted by score (highest to lowest)
    action_list = [key for key, value in sorted(action_score.items(), key=lambda item: item[1], reverse=True)]
    action_node = ActionSelectorNode(action_list)
    return action_node


def learn_action_using_GP(e, agent):
    """return subtree learned with Genetic Programming"""
    pass


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


def fitness_score(e, agent,
                  steps=TRY_ACTION_STEPS, samples=TRY_ACTION_SAMPLES, action=ACT_NOACTION):
    """fitness score for learning algorithm
    consider change in speed and road availability after T steps
    """
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
        if action is None:
            action = agent.tick(state)
        state, _, _, _ = e_.step(ACT_TO_ACTIDX[action])
        agent.update_condition_checker(state[0])
        agent.update_blackboard()
        # simulate
        _ = play_episode(e_, agent, steps=steps, reset=False)

        # score for availability after T steps
        state = e_._render_state(e_.state)[0]
        agent.update_condition_checker(state)
        agent.update_blackboard()
        can_accelerate = agent.condition_checker.can_accelerate()
        can_switch_left = agent.condition_checker.can_switch_left()
        can_switch_right = agent.condition_checker.can_switch_right()
        avail_score = 0
        if can_accelerate:
            avail_score += CAN_ACCELERATE_SCORE
        elif can_switch_left or can_switch_right:
            avail_score += CAN_SWITCH_LANE
        else:
            pass
        # speed score: speed difference
        after_speed = agent.blackboard.speed
        speed_score = min(1, max(after_speed - init_speed, -1))
        # total score
        score.append(speed_score + avail_score)

    return np.mean(score)


def fitness_score_v2(e, agent,
                     steps=TRY_ACTION_STEPS, samples=TRY_ACTION_SAMPLES, action=ACT_NOACTION):
    """fitness score version2: consider mean_speed within T steps"""
    # initialize
    score = []

    # simulation loops
    for sample in range(samples):
        # deep copy env
        e_ = copy.deepcopy(e)
        # try action
        if action is None:
            state = e._render_state(e.state)
            action = agent.tick(state[0])
        # step
        _ = e_.step(ACT_TO_ACTIDX[action])
        # simulate
        mean_speed = play_episode(e_, agent, steps=steps, reset=False)
        # score
        score.append(mean_speed / MAX_SPEED)

    return np.mean(score)


def hash_action_node(action_node):
    """string key represents ActionSequenceNode
    (not compatible to for GP-learned action node)"""
    # create key for action node
    key = ''
    for action in action_node.children:
        key += action.name + '_'
    key = key[:-1]  # get rid of the last '_'
    return key


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=int, default=1, help="Train algorithm version: [1, 2, 3]")
    args = parser.parse_args()

    # initialize env
    e = env.DeepTraffic(lanes_side=LANES_SIDE,
                        patches_ahead=PATCHES_AHEAD,
                        patches_behind=PATCHES_BEHIND,
                        history=HISTORY,
                        obs=OBS)
    e.reset()

    # initialize agent
    agent = GeneticProgrammingBehaviorTreeAgent()
    agent.reset()

    # train
    train_algs = (None, train_GP_BT, train_GP_BT_v2, train_GP_BT_v3)
    train_algs[args.version](e, agent, episodes=TRAIN_EPISODES, steps=PLAY_EPISODE_STEPS)

    # save
    agent.save(name='GP-BT_v%d' % args.version)
