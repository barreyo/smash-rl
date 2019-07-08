
import json
from typing import List, Union

from framework.agent import Agent
from framework.devices.device import Device
from framework.observation import Observation


class GameStats():

    def __init__(self, file_name: Union[str, None]):
        self.fp = None
        self.data_store = []
        self.file_name = file_name

    def append(self, total_reward: float, total_timesteps: int):
        self.data_store.append(
            dict(total_reward=total_reward, total_timesteps=total_timesteps))
        self.dump()

    def dump(self):
        if self.file_name is not None:
            with open(self.file_name, 'w') as f:
                json.dump(self.data_store, f)

    def __del__(self):
        self.fp = None
        self.data_store = None


class Game():

    def __init__(self, device: Device, agents: List[Agent] = [],
                 stats_file=None):
        self.device = device
        self.agents = agents
        self.stats = GameStats(stats_file)

    def game_update(self, observation: Observation):
        raise NotImplementedError("Please implement me")

    def meta_update(self, update_data):
        raise NotImplementedError("Please implement me")

    def reset(self):
        raise NotImplementedError("Please implement me")

    def hard_reset(self):
        raise NotImplementedError("Please implement me")
