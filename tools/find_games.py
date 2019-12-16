"""Prints a .slp file frame by frame."""

import logging
import os
from multiprocessing import Pool

from slippi import Game
from slippi.id import CSSCharacter, Stage

STAGES = [Stage.BATTLEFIELD, Stage.FINAL_DESTINATION]
CHARACTERS = [CSSCharacter.FOX]

log = logging.getLogger(__name__)


def is_valid(f):
    try:
        log.info(f"Scanning {f}")
        game = Game(os.path.join('./data', f))
        all_characters = [p.character for p in game.start.players
                          if p is not None]

        if game.start.stage in STAGES and \
                len(set(all_characters) & set(CHARACTERS)) > 0:
            return True
        return False
    except Exception:
        return False


def _main():
    p = Pool(8)
    files = [x for x in os.listdir('./data/') if x.endswith('.slp')]
    p.map(is_valid, files)
    p.terminate()
    p.join()


if __name__ == '__main__':
    _main()
