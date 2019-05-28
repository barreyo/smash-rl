"""Prints a .slp file frame by frame."""

from slippi import Game
from slippi.event import Buttons
from framework.games.ssbm.ssbm_action import SSBMAction
from framework.games.ssbm.ssbm_observation import SSBMObservation


def bitfield(n):
    return [1 if digit == '1' else 0 for digit in bin(n)[2:]]


def _main():
    games = [Game('Game_20190224T233757.slp'),
             Game('Game_20190224T234808.slp'),
             Game('Game_20190224T222630.slp'),
             Game('Game_20190224T231855.slp')]
    states = []
    button_set = set()
    possible_actions = []
    for game in games:
        print(game.start)
        print(game.start.players)

        for frame in game.frames:
            print(frame.ports)
            # ICs is never played so do not worry about follower
            try:
                p1_pre = frame.ports[0].leader.pre
                p2_pre = frame.ports[2].leader.pre

                p1_post = frame.ports[0].leader.post
                p2_post = frame.ports[2].leader.post
            except AttributeError:
                continue

            frame_obs = SSBMObservation((p1_pre.position.x, p1_pre.position.y),
                                        (p2_pre.position.x, p2_pre.position.y),
                                        p1_post.stocks, p2_post.stocks,
                                        p1_post.damage, p2_post.damage)
            states.append(frame_obs)

            button_set.add(p1_pre.buttons.logical)
            button_set.add(p2_pre.buttons.logical)
            # print(f'B: {p1_pre.buttons}')

            # print(f'i={frame.index} S={frame_obs}')

    # print(len(button_set))

    for b in button_set:
        res = SSBMAction()
        if b & Buttons.Logical.TRIGGER_ANALOG:
            res.state[0] = 1
        if b & Buttons.Logical.CSTICK_RIGHT:
            res.state[1] = 1
        if b & Buttons.Logical.CSTICK_LEFT:
            res.state[2] = 1
        if b & Buttons.Logical.CSTICK_DOWN:
            res.state[3] = 1
        if b & Buttons.Logical.CSTICK_UP:
            res.state[4] = 1
        if b & Buttons.Logical.JOYSTICK_RIGHT:
            res.state[5] = 1
        if b & Buttons.Logical.JOYSTICK_LEFT:
            res.state[6] = 1
        if b & Buttons.Logical.JOYSTICK_DOWN:
            res.state[7] = 1
        if b & Buttons.Logical.JOYSTICK_UP:
            res.state[8] = 1
        if b & Buttons.Logical.Y:
            res.state[9] = 1
        if b & Buttons.Logical.X:
            res.state[10] = 1
        if b & Buttons.Logical.B:
            res.state[11] = 1
        if b & Buttons.Logical.A:
            res.state[12] = 1
        if b & Buttons.Logical.L:
            res.state[13] = 1
        if b & Buttons.Logical.R:
            res.state[14] = 1
        if b & Buttons.Logical.Z:
            res.state[15] = 1

        possible_actions.append(res)
        print(res)

    print(len(possible_actions))
    print(len(set(possible_actions)))


if __name__ == '__main__':
    _main()
