"""Prints a .slp file frame by frame."""

from slippi import Game
from smashrl.action import Action
from smashrl.observation import Observation


def _main():
    game = Game('Game_20190224T233757.slp')
    states = []

    for frame in game.frames:
        # ICs is never played so do not worry about follower
        p1_pre = frame.ports[0].leader.pre
        p2_pre = frame.ports[2].leader.pre

        p1_post = frame.ports[0].leader.post
        p2_post = frame.ports[2].leader.post

        frame_obs = Observation((p1_pre.position.x, p1_pre.position.y),
                                (p2_pre.position.x, p2_pre.position.y),
                                p1_post.stocks, p2_post.stocks, p1_post.damage,
                                p2_post.damage)
        states.append(frame_obs)

        print(f'i={frame.index} S={frame_obs}')


if __name__ == '__main__':
    _main()
