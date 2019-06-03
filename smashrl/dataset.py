
import logging
import os
import pickle
import sys
from multiprocessing import Pool
from pathlib import Path
from typing import List, Tuple

from framework.games.ssbm.ssbm_action import SSBMAction
from framework.games.ssbm.ssbm_observation import Position, SSBMObservation
from slippi import Game
from slippi.event import Buttons
from slippi.id import InGameCharacter, Stage

VALID_CHARACTERS = {InGameCharacter.FOX}
VALID_STAGES = {Stage.BATTLEFIELD, Stage.FINAL_DESTINATION}
DEFAULT_STOCK = 3

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def is_valid_stage(stage: Stage) -> bool:  # noqa
    return stage in VALID_STAGES


def is_valid_character(char: InGameCharacter) -> bool:  # noqa
    return char in VALID_CHARACTERS


def create_action_from_button(logical):
    return SSBMAction(
        trigger=logical & Buttons.Logical.TRIGGER_ANALOG,
        cstick_right=logical & Buttons.Logical.CSTICK_RIGHT,
        cstick_left=logical & Buttons.Logical.CSTICK_LEFT,
        cstick_down=logical & Buttons.Logical.CSTICK_DOWN,
        cstick_up=logical & Buttons.Logical.CSTICK_UP,
        joystick_right=logical & Buttons.Logical.JOYSTICK_RIGHT,
        joystick_left=logical & Buttons.Logical.JOYSTICK_LEFT,
        joystick_down=logical & Buttons.Logical.JOYSTICK_DOWN,
        joystick_up=logical & Buttons.Logical.JOYSTICK_UP,
        y=logical & Buttons.Logical.Y,
        x=logical & Buttons.Logical.X,
        b=logical & Buttons.Logical.B,
        a=logical & Buttons.Logical.A,
        l=logical & Buttons.Logical.L,  # noqa
        r=logical & Buttons.Logical.R,
        z=logical & Buttons.Logical.Z
    )


def format_training_data(game: Game) -> List[List[
        Tuple[SSBMObservation, SSBMAction]]]:
    """
    Grab a bunch of games and split out each game into training format.

    Each frame in the game is turned into an observation and action tuple that
    can be used to 'replay' a game and train an agent. Note that if both
    players in the game are of the correct character they will both be added
    as separate training sessions.

    NOTE: Only formats games that have valid characters and a valid stage.

    Arguments:
    game -- A Slippi game

    Returns:
    A list of lists of tuples (SSBMObservation, SSBMAction[Action])

    """
    training_data = list()

    if not is_valid_stage(game.start.stage):
        log.info(f'Skipping game... not a valid stage({game.start.stage})')
        return []

    s1, s2 = list(), list()

    for frame in game.frames:
        try:
            p1_pre = frame.ports[0].leader.pre
            p2_pre = frame.ports[2].leader.pre

            p1_post = frame.ports[0].leader.post
            p2_post = frame.ports[2].leader.post
        except AttributeError:
            return []

        if is_valid_character(p1_post.character):
            p1_obs = SSBMObservation(Position(p1_pre.position.x,
                                                p1_pre.position.y),
                                        Position(p2_pre.position.x,
                                                p2_pre.position.y),
                                        p1_post.stocks, p2_post.stocks,
                                        p1_post.damage, p2_post.damage)
            p1_action = create_action_from_button(p1_pre.buttons.logical)
            p1_frame_tuple = (p1_obs, p1_action)
            s1.append(p1_frame_tuple)

        if is_valid_character(p2_post.character):
            p2_obs = SSBMObservation(Position(p2_pre.position.x,
                                                p2_pre.position.y),
                                        Position(p1_pre.position.x,
                                                p1_pre.position.y),
                                        p2_post.stocks, p1_post.stocks,
                                        p2_post.damage, p1_post.damage)
            p2_action = create_action_from_button(p2_pre.buttons.logical)
            p2_frame_tuple = (p2_obs, p2_action)
            s2.append(p2_frame_tuple)

    if s1:
        log.info('Adding game session for P1')
        training_data.append(s1)

    if s2:
        log.info('Adding game session for P2')
        training_data.append(s2)

    if s1 or s2:
        winner = 'p1' if frame.ports[0].leader.post.stocks > 0 else 'p2'
        log.info(f'Winner: {winner}')

    return training_data


def read_game(path: str) -> Game:
    if not path.endswith('.slp'):
        return None
    try:
        log.debug(f"Reading in game: {path}")
        game = Game(path)
        return game if is_valid_stage(game.start.stage) else None
    except ValueError:
        pass


def read_games(folder: str, max_games: int) -> List[Game]:
    p = Pool(8)
    files = [os.path.join(folder, x)
             for x in os.listdir(folder) if x.endswith('.slp')]
    if max_games != -1:
        files = files[0:max_games]
    games = p.map(read_game, files)
    p.terminate()
    p.join()

    # filter out bad games
    games = [g for g in games if g is not None]

    return games


def dump_to_disk(output: str, games: List[Game]):
    # log.info(f"Collecting training data from: {len(games)} games...")
    # data = format_training_data(games)
    # log.info(f"Found: {len(data)} valid games...")
    # log.info(f"Writing training data to: {output}")
    log.info(f"Found {len(games)} valid games")
    Path(os.path.dirname(output)).mkdir(parents=True, exist_ok=True)
    with open(output, 'wb') as f:
        pickle.dump(games, f)


def _main():
    game_folder = sys.argv[1]
    output = sys.argv[2]
    max_games = int(sys.argv[3]) if len(sys.argv) == 4 else -1

    games = read_games(game_folder, max_games)
    dump_to_disk(output, games)


if __name__ == "__main__":
    _main()
