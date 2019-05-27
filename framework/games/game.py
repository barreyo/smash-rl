
from typing import List

from framework.agent import Agent
from framework.devices.device import Device


class Game():

    def __init__(self, device: Device, agents: List[Agent] = []):
        self.device = device
        self.agents = agents
