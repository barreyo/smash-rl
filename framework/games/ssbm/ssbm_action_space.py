
from framework.action_space import DiscreteActionSpace
from framework.games.ssbm.ssbm_action import VALID_ACTIONS, SSBMAction


class SSBMActionSpace(DiscreteActionSpace):

    def __init__(self):
        actions = [SSBMAction(*v) for v in VALID_ACTIONS]
        super().__init__(actions)
