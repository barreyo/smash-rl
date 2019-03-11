"""Prints a .slp file frame by frame."""

from slippi import Game


def _main():
    game = Game('Game_20190224T233757.slp')

    for frame in game.frames:
        data = frame.ports[0].leader  # see also: port.follower (ICs)
        print(f'Player 1 pos: {frame.ports[0].position}    Player 2 pos: {frame.ports[1].position})


if __name__ == '__main__':
    _main()
