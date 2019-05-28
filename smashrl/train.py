"""Handle data formatting from replays and offline training of the Agent."""

import logging
import pickle
import sys
from typing import List

import numpy as np

from framework.agent import Agent
from framework.games.ssbm.ssbm_reward import SimpleSSBMReward
from framework.reward import Reward
from slippi import Game
from smashrl.dataset import format_training_data
from smashrl.ssbm_agent import SSBMAgent

log = logging.getLogger(__name__)


def run_offline_training_sequence(
        agent: Agent,
        reward_calculator: Reward,
        games: List[Game]) -> None:
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

    formatted_games = format_training_data(games)

    for game_idx, game in enumerate(formatted_games):
        obs, action = game[0]
        observations = [obs]
        losses = []
        rewards = []

        log.info(f"Starting game: {game_idx + 1}/{len(formatted_games)}")
        for ts, (new_obs, next_action) in enumerate(game[1:]):

            reward = reward_calculator.cost(new_obs, observations, ts)
            rewards.append(reward)
            done = float(ts == (len(game) - 1))

            loss = agent.learn(obs, new_obs, action, reward, done)
            losses.append(loss)

            # print(action)

            if ts % 1000 == 0:
                log.info(f"TS: {ts}, Loss: {loss}, "
                         f"Avg Reward: {np.average(rewards)}")

            obs, action = new_obs, next_action

        log.info("Training summary:")
        log.info(f"Average loss: {np.average(losses)}")
        log.info(f"Average reward: {np.average(rewards)}")
        log.info(f"Total TS: {len(game)}")
        log.info("=====================")

        agent.save()


def _main():
    with open(sys.argv[1], 'rb') as f:
        dataset = pickle.load(f)

    agent = SSBMAgent()

    # TODO: Load pre-trained model
    # agent.load()

    reward = SimpleSSBMReward()
    run_offline_training_sequence(agent, reward, dataset)

    agent.save()


if __name__ == "__main__":
    _main()
