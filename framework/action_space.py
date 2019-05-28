
from typing import List

import numpy as np

from framework.action import Action, DiscreteAction


class ActionSpace():

    def __init__(self, actions: List[Action]):
        self.actions = actions

    @property
    def n_actions(self) -> int:
        return len(self.actions)


class ContinuousActionSpace(ActionSpace):

    def __init__(self, actions: List[Action]):
        super().__init__(actions)


class DiscreteActionSpace(ActionSpace):

    def __init__(self, actions: List[Action]):
        super().__init__(actions)

    def action_to_index(self, index: int) -> Action:
        return self.actions[index]

    def random_action(self) -> DiscreteAction:
        return np.random.choice(self.actions)
