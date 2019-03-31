import os
import sys
import logging
import pickle
from typing import List, Tuple
from pathlib import Path
from multiprocessing import Pool

from slippi import Game
from slippi import Game
from slippi.id import InGameCharacter, Stage

from framework.games.ssbm.ssbm_observation import SSBMObservation
from framework.games.ssbm.ssbm_action import SSBMAction

VALID_CHARACTERS = {InGameCharacter.FOX}
VALID_STAGES = {Stage.BATTLEFIELD, Stage.FINAL_DESTINATION}
DEFAULT_STOCK = 3

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def is_valid_stage(stage: Stage) -> bool:  # noqa
    return stage in VALID_STAGES


def is_valid_character(char: InGameCharacter) -> bool:  # noqa
    return char in VALID_CHARACTERS


def format_training_data(games: List[Game]) -> List[List[
        Tuple[SSBMObservation, SSBMAction]]]:
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
    A list of lists of tuples (SSBMObservation, SSBMAction[Action])

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
                p1_obs = SSBMObservation((p1_pre.position.x, p1_pre.position.y),
                                     (p2_pre.position.x, p2_pre.position.y),
                                     p1_post.stocks, p2_post.stocks,
                                     p1_post.damage, p2_post.damage)
                p1_action = SSBMAction()
                p1_frame_tuple = (p1_obs, p1_action)
                s1.append(p1_frame_tuple)

            if is_valid_character(p2_post.character):
                p2_obs = SSBMObservation((p2_pre.position.x, p2_pre.position.y),
                                     (p1_pre.position.x, p1_pre.position.y),
                                     p2_post.stocks, p1_post.stocks,
                                     p2_post.damage, p1_post.damage)
                p2_action = SSBMAction()
                p2_frame_tuple = (p2_obs, p2_action)
                s2.append(p2_frame_tuple)

        if s1:
            log.info('Adding game session for P1')
            training_data.append(s1)

        if s2:
            log.info('Adding game session for P2')
            training_data.append(s2)

    return training_data

def read_game(path: str) -> Game:
    if not path.endswith('.slp'):
        return None
    try:
        log.debug(f"Reading in game: {path}")
        return Game(path)
    except ValueError:
        pass


def read_games(folder: str) -> List[Game]:
    p = Pool(8)
    files = [os.path.join(folder, x) for x in os.listdir(folder) if x.endswith('.slp')]
    games = p.map(read_game, files)
    p.terminate()
    p.join()

    # filter out bad games
    games = [g for g in games if g is not None]

    return games


def dump_to_disk(output: str, games: List[Game]):
    log.info(f"Collecting training data from: {len(games)} games...")
    data = format_training_data(games)
    log.info(f"Found: {len(data)} valid games...")
    log.info(f"Writing training data to: {output}")

    Path(os.path.dirname(output)).mkdir(parents=True, exist_ok=True)
    with open(output, 'wb') as f:
        pickle.dump(data, f)


def _main():
    game_folder = sys.argv[1]
    output = sys.argv[2]

    games = read_games(game_folder)
    dump_to_disk(output, games)


if __name__ == "__main__":
    _main()