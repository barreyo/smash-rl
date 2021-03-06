"""Classes denoting different actions."""

import inspect
import os
from typing import Union

import numpy as np

from framework.action import Action
from slippi.event import Buttons

VALID_ACTIONS = np.load(os.path.dirname(__file__) + '/ssbm_actions.npy')
N_LOGICAL_INPUTS = len(VALID_ACTIONS[0])
N_ACTIONS = len(VALID_ACTIONS)
STATE_TO_INDEX_LOOKUP = {
    tuple(vl): idx for idx, vl in enumerate(VALID_ACTIONS)
}

STATE_TO_SLIPPI = [
    Buttons.Logical.TRIGGER_ANALOG,
    Buttons.Logical.CSTICK_RIGHT,
    Buttons.Logical.CSTICK_LEFT,
    Buttons.Logical.CSTICK_DOWN,
    Buttons.Logical.CSTICK_UP,
    Buttons.Logical.JOYSTICK_RIGHT,
    Buttons.Logical.JOYSTICK_LEFT,
    Buttons.Logical.JOYSTICK_DOWN,
    Buttons.Logical.JOYSTICK_UP,
    Buttons.Logical.Y,
    Buttons.Logical.X,
    Buttons.Logical.B,
    Buttons.Logical.A,
    Buttons.Logical.L,
    Buttons.Logical.R,
    Buttons.Logical.Z,
]


class SSBMAction(Action):
    """Denoting an action taken in a single frame."""

    def __init__(self, trigger: int = 0, cstick_right: int = 0,
                 cstick_left: int = 0, cstick_down: int = 0,
                 cstick_up: int = 0, joystick_right: int = 0,
                 joystick_left: int = 0, joystick_down: int = 0,
                 joystick_up: int = 0, y: int = 0, x: int = 0, b: int = 0,
                 a: int = 0, l: int = 0, r: int = 0, z: int = 0):
        """
        Create a controller state object.

        Each entry is either 0 or 1 denoting if the button or logical input is
        active. Defaults to all zeros, aka 'idle'.
        """
        frame = inspect.currentframe()
        args, _, _, _ = inspect.getargvalues(frame)
        self.named_state = args[1:]
        self.state = np.array([trigger, cstick_right, cstick_left, cstick_down,
                               cstick_up, joystick_right, joystick_left,
                               joystick_down, joystick_up, y, x, b, a, l,
                               r, z])
        self.__clamp_state()
        self.__simplify_state()

    def __clamp_state(self):
        self.state = [1 if v > 0 else 0 for v in self.state]

    def __simplify_state(self):
        self.state = simplify_action(self.state)

    @classmethod
    def from_index(cls, index: int):
        return cls(*VALID_ACTIONS[index])

    def as_array(self) -> np.array:
        """Return the controller state as 1-dimensional(1,) numpy array."""
        array = np.zeros(N_ACTIONS)
        array[self.as_index()] = 1
        return array

    def as_index(self) -> int:
        """Return the Action index of this controller state."""
        return reverse_action_lookup(self.state)

    def as_slippi_bitmask(self) -> Buttons.Logical:
        """Return action(s) as Slippi bitmask."""
        res = Buttons.Logical(Buttons.Logical.NONE)
        for i, mask in enumerate(STATE_TO_SLIPPI):
            if self.state[i]:
                res |= mask

        return res

    def __str__(self):  # noqa
        tupled_actions = zip(self.named_state, self.state)
        active = [a for a, b in tupled_actions if b != 0]
        if not active:
            return 'Idle'
        return 'Pressing: ' + ', '.join(active)


def reverse_action_lookup(controller_state: Union[np.array, SSBMAction]) -> int:  # noqa
    """
    Lookup the action index of this controller state.

    Arguments:
    controller_state -- A numpy array or a ControllerState object
    """
    if isinstance(controller_state, SSBMAction):
        return controller_state.as_index()

    return STATE_TO_INDEX_LOOKUP[tuple(controller_state)]


def simplify_action(action: np.array) -> np.array:
    # A before B
    if action[11] + action[12] > 1:
        action[11] = 0
        action[12] = 1

    # C stick before joystick
    if action[1] + action[2] + action[3] + action[4] == 1:
        action[5] = 0
        action[6] = 0
        action[7] = 0
        action[8] = 0

    # R before L
    if action[13] == 1:
        action[14] = 1
        action[13] = 0

    # Y before X
    if action[9] == 1:
        action[10] = 1
        action[9] = 0

    # Z before anything
    if action[15] == 1:
        action = [0] * 16
        action[15] = 1

    # Only joystick with block
    if action[14] == 1:
        joystick = action[5:9].copy()
        action = [0] * 16
        action[14] = 1
        action[5:9] = joystick

    return action
