# DeepTraffic
LANES_SIDE = 2
PATCHES_AHEAD = 15
PATCHES_BEHIND = 5
HISTORY = 1
OBS = 'conv'
SPEED_FACTOR = 2000  # SPEED_FACTOR * state_value = real_speed
MAX_SPEED = 120


# ConditionChecker
SAFETY_FRONT = 4
SWITCH_LANE_SAFETY_FRONT = 5
MIN_SAFETY_SPEED = 10


# BehaviorTree
ACT_NOACTION = "noAction"
ACT_ACCELERATE = "accelerate"
ACT_DECELERATE = "decelerate"
ACT_SWITCHLEFT = "goLeft"
ACT_SWITCHRIGHT = "goRight"
ACT_LEARN = "learnAction"
SAFETY_ACTION = ACT_ACCELERATE


# Agent
ACT_TO_ACTIDX = {
    ACT_NOACTION: 0,
    ACT_ACCELERATE: 1,
    ACT_DECELERATE: 2,
    ACT_SWITCHLEFT: 3,
    ACT_SWITCHRIGHT: 4
}
ACTIDX_TO_ACT = { 
    ACT_TO_ACTIDX[key]:key for key in ACT_TO_ACTIDX
}
BTMODELPATH = "saves/"


# DQN
DQNMODELPATH = "deep_traffic/saves/BTconfig-BTconfig/best_72.95.dat"


# Runner
PLAY_EPISODE_STEPS = 200
PLAY_EPISODE_SLEEP_TIME = 0.25
CHANGE_ACT_SLEEP_TIME = 2.0
FULL_VISUALIZE = False
PERFORMANCE_TEST_EPISODES = 100
SAVEPATH = "results/"


# Train
TRAIN_EPISODES = 30
TRY_ACTION_STEPS = 10
TRY_ACTION_SAMPLES = 5
CAN_ACCELARATE_SCORE = 0.5
CAN_SWITCH_LANE = 0.25
