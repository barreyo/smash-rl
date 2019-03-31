"""Handle data formatting from replays and offline training of the Agent."""

import sys
import logging
import pickle
from typing import List, Tuple

# from smashrl.action import ControllerState
# from smashrl.observation import Observation
# from smashrl.reward_function import SimpleSSMMRewardState

log = logging.getLogger(__name__)

def run_offline_training_sequence(agent, cost_function, games):
    """
    Run a training sequence of a set of games.

    The resulting neural network is stored on disc and can be loaded for future
    play.

    Arguments:
    agent -- The RL Agent object to train
    cost_function -- A reward(cost) function object that tracks state of
        rewards and gives the cost for each simulation step
    games -- A list of Slippi game objects to use for training
    """
    # Stock should be read from Replay
    # reward_state = SimpleSSMMRewardState(DEFAULT_STOCK)

    log.info('Starting training sequence')
    log.info('Formatting data')


def _main():
    with open(sys.argv[1], 'rb') as f:
        dataset = pickle.load(f)

if __name__ == "__main__":
    _main()