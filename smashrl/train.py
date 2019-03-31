"""Handle data formatting from replays and offline training of the Agent."""

import logging
from typing import List, Tuple

from slippi import Game
from slippi.id import InGameCharacter, Stage
from smashrl.action import ControllerState
from smashrl.observation import Observation
from smashrl.reward_function import SimpleSSMMRewardState

log = logging.getLogger(__name__)

VALID_CHARACTERS = {InGameCharacter.FOX}
VALID_STAGES = {Stage.BATTLEFIELD, Stage.FINAL_DESTINATION}
DEFAULT_STOCK = 3


def is_valid_stage(stage: Stage) -> bool:  # noqa
    return stage in VALID_STAGES


def is_valid_character(char: InGameCharacter) -> bool:  # noqa
    return char in VALID_CHARACTERS


def format_training_data(games: List[Game]) -> List[List[
        Tuple[Observation, ControllerState]]]:
    """
    Grab a bunch of games and split out each game into training format.

    Each frame in the game is turned into an observation and action tuple that
    can be used to 'replay' a game and train an agent. Note that if both
    players in the game are of the correct character they will both be added
    as separate training sessions.

    NOTE: Only formats games that have valid characters and a valid stage.

    Arguments:
    games -- A list of Slippi games

    Returns:
    A list of lists of tuples (Observation, ControllerState[Action])

    """
    training_data = list()

    for game in games:

        if not is_valid_stage(game.start.stage):
            log.info(f'Skipping game... not a valid stage({game.start.stage})')
            continue

        s1, s2 = list(), list()

        for frame in game.frames:
            try:
                p1_pre = frame.ports[0].leader.pre
                p2_pre = frame.ports[2].leader.pre

                p1_post = frame.ports[0].leader.post
                p2_post = frame.ports[2].leader.post
            except AttributeError:
                continue

            if is_valid_character(p1_post.character):
                p1_obs = Observation((p1_pre.position.x, p1_pre.position.y),
                                     (p2_pre.position.x, p2_pre.position.y),
                                     p1_post.stocks, p2_post.stocks,
                                     p1_post.damage, p2_post.damage)
                p1_action = ControllerState()
                p1_frame_tuple = (p1_obs, p1_action)
                s1.append(p1_frame_tuple)

            if is_valid_character(p2_post.character):
                p2_obs = Observation((p2_pre.position.x, p2_pre.position.y),
                                     (p1_pre.position.x, p1_pre.position.y),
                                     p2_post.stocks, p1_post.stocks,
                                     p2_post.damage, p1_post.damage)
                p2_action = ControllerState()
                p2_frame_tuple = (p2_obs, p2_action)
                s2.append(p2_frame_tuple)

        if s1:
            log.info('Adding game session for P1')
            training_data.append(s1)

        if s2:
            log.info('Adding game session for P2')
            training_data.append(s2)

    return training_data


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
    reward_state = SimpleSSMMRewardState(DEFAULT_STOCK)

    log.info('Starting training sequence')
    log.info('Formatting data')
