"""Prints a .slp file frame by frame."""

import os
import numpy as np

from slippi import Game
from slippi.event import Buttons
from framework.games.ssbm.ssbm_action import SSBMAction, STATE_TO_INDEX_LOOKUP
from framework.games.ssbm.ssbm_observation import SSBMObservation


def bitfield(n):
    return [1 if digit == '1' else 0 for digit in bin(n)[2:]]


def read_games(folder: str):
    files = [os.path.join(folder, x)
             for x in os.listdir(folder) if x.endswith('.slp')]

    for game in files:
        try:
            yield len(files), Game(game)
        except Exception:
            yield len(files), None


def _main():
    games = read_games('./data')

    states = []
    button_set = set()
    possible_actions = set()
    result = []
    for n, (max_g, game) in enumerate(games):
        print(f'Working on game {n + 1} of {max_g}')

        if game is None:
            continue

        for frame in game.frames:
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

        possible_actions.add(tuple(res.state))

    print(f'Actions found: {len(possible_actions)}')

    for possible in possible_actions:
        action = np.array(list(possible))
        result.append(action)
        # print(f'np.array([{str(possible)[1:-1]}]),')

    np.save('new_actions_file', np.array(result))


if __name__ == '__main__':
    _main()
