"""Handle data formatting from replays and offline training of the Agent."""

import logging
import pickle
import sys
from typing import List, Tuple
import numpy as np

from framework.games.ssbm.ssbm_reward import SimpleSSBMReward

from smashrl.ssbm_agent import SSBMAgent
from smashrl.dataset import format_training_data


log = logging.getLogger(__name__)


def run_offline_training_sequence(agent, reward_calculator, games):
    """
    Run a training sequence of a set of games.

    The resulting neural network is stored on disc and can be loaded for future
    play.

    Arguments:
    agent -- The RL Agent object to train
    reward -- A reward class with a cost function
    games -- A list of Slippi game objects to use for training
    """

    log.info('Starting training sequence')
    log.info('Formatting data')

    for game_idx, game in enumerate(format_training_data(games)):
        obs, action = game[0]
        observations = [obs]
        losses = []
        rewards = []

        log.info(f"Starting game: {game_idx}/{len(games)}")
        for ts, (new_obs, next_action) in enumerate(game[1:]):

            reward = reward_calculator.cost(new_obs, observations, ts)
            rewards.append(reward)
            done = float(ts == (len(game) - 1))

            loss = agent.learn(obs, new_obs, action, reward, done)
            losses.append(loss)
            if ts % 100 == 0:
                log.info(f"TS: {ts}, Loss: {loss}")

            obs, action = new_obs, next_action

        log.info("Training summary:")
        log.info(f"Average loss: {np.average(losses)}")
        log.info(f"Average reward: {np.average(rewards)}")
        log.info(f"Total TS: {len(game)}")
        log.info("=====================")



def _main():
    with open(sys.argv[1], 'rb') as f:
        dataset = pickle.load(f)

    agent = SSBMAgent()

    # TODO: Load pre-trained model
    # agent.load()

    reward = SimpleSSBMReward()
    run_offline_training_sequence(agent, reward, dataset)

    # agent.save()


if __name__ == "__main__":
    _main()
