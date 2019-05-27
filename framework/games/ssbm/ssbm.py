
from typing import List

from framework.agent import Agent
from framework.devices.device import Device
from framework.games.game import Game


# TODO: Add all SSBM sub classes, use this as a configuration object for the
#       agent
class SSBMGame(Game):

    def __init__(self, device: Device, agents: List[Agent] = []):

        return super().__init__(device, agents=agents)
