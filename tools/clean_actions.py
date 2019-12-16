
import logging

import numpy as np

log = logging.getLogger(__name__)

actions = np.load('./framework/games/ssbm/ssbm_actions.npy')

actions = list([list(x) for x in actions])

log.info(len(actions))

for i, r in enumerate(actions):

    # A before B
    if r[11] + r[12] > 1:
        actions[i][11] = 0
        actions[i][12] = 1

    # C stick before joystick
    if r[1] + r[2] + r[3] + r[4] == 1:
        actions[i][5] = 0
        actions[i][6] = 0
        actions[i][7] = 0
        actions[i][8] = 0

    # R before L
    if r[13] == 1:
        actions[i][14] = 1
        actions[i][13] = 0

    # Y before X
    if r[9] == 1:
        actions[i][10] = 1
        actions[i][9] = 0

    # Z before anything
    if r[15] == 1:
        actions[i] = [0] * 16
        actions[i][15] = 1

    if r[14] == 1:
        joystick = actions[i][5:9].copy()
        actions[i] = [0] * 16
        actions[i][14] = 1
        actions[i][5] = joystick[0]
        actions[i][6] = joystick[1]
        actions[i][7] = joystick[2]
        actions[i][8] = joystick[3]

actions = set([tuple(a) for a in actions])

actions = np.array([np.array(a) for a in actions])
np.save('./framework/games/ssbm/ssbm_actions.npy', actions)

log.info(len(actions))
