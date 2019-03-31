"""The actual RL Agent"""

from smashrl.action import ControllerState
from smashrl.observation import Observation
from framework.agent import Agent

class SSBMAgent(Agent):

    def __init__(self):
        pass

    def get_action(self, observation: Observation) -> ControllerState:
        pass
