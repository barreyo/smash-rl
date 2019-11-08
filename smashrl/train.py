"""Handle data formatting from replays and offline training of the Agent."""

import logging
import os
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


def read_games(folder: str):
    files = [os.path.join(folder, x)
             for x in os.listdir(folder) if x.endswith('.slp')]

    for game in files:
        try:
            yield len(files), Game(game)
        except Exception:
            yield len(files), None


def run_offline_training_sequence(
        agent: Agent,
        reward_calculator: Reward,
        games: List[Game],
        per_game_iteration: int = 1) -> None:
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

    for game_idx, (max_g, unformatted_game) in enumerate(games):

        if unformatted_game is None:
            continue

        formatted_games = format_training_data(unformatted_game)

        for game_iteration in range(per_game_iteration):
            log.info(
                f"Training on game: {game_idx + 1}/{max_g}, "
                f"iteration: {game_iteration + 1}/{per_game_iteration}")

            for game in formatted_games:

                obs, action = game[0]
                observations = [obs]
                losses = []
                rewards = []

                for ts, (new_obs, next_action) in enumerate(game):

                    reward = reward_calculator.cost(new_obs, observations, ts)
                    rewards.append(reward)
                    done = float(ts == (len(game) - 1))

                    loss = agent.learn(obs, new_obs, action, reward, done)
                    losses.append(loss)

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
    dataset = read_games(sys.argv[1])

    agent = SSBMAgent()

    # TODO: Load pre-trained model
    # agent.load()

    reward = SimpleSSBMReward()
    run_offline_training_sequence(
        agent, reward, dataset, per_game_iteration=10)

    agent.save()


if __name__ == "__main__":
    _main()
