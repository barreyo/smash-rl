"""Prints a .slp file frame by frame."""

from slippi import Game
from slippi.id import Stage, CSSCharacter
import os

def _main():

    STAGES = [Stage.BATTLEFIELD, Stage.FINAL_DESTINATION]
    CHARACTERS = [CSSCharacter.FOX]

    valid_replays = []
    invalid_replays = []


    for f in os.listdir('./data/'):
        if not f.endswith('.slp'):
            continue
        try:
            game = Game(os.path.join('./data', f))
            all_characters = [p.character for p in game.start.players if p is not None]

            if game.start.stage in STAGES and len(set(all_characters) & set(CHARACTERS)) > 0:
                valid_replays.append(f)
            else:
                invalid_replays.append(f)
        except Exception:
            invalid_replays.append(f)
            print("Could not parse: {}".format(f))

    print(f"Found {len(valid_replays)} valid replays")
    for v in valid_replays:
        print(v)

if __name__ == '__main__':
    _main()
