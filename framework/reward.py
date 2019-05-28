
from typing import List

from framework.observation import Observation


class Reward():

    def cost(self,
             current_observation: Observation,
             historical_observations: List[Observation],
             step: int) -> float:
        raise NotImplementedError('Implement this')
