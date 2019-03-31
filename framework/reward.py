from framework.observation import Observation
from typing import List

class Reward():

    def cost(self, current_observation: Observation, historical_observations: List[Observation], step: int) -> float:
        raise NotImplementedError('Implement this')