"""Cost/reward function implementations."""

from typing import List

from framework.observation import Observation
from framework.reward import Reward


class SimpleSSBMReward(Reward):

    LIFE_LOSS_COST = -1.0
    LIFE_INFLICT_COST = 1.0
    STOCK_LOSS_COST = -100.0
    STOCK_INFLICT_COST = 100.0
    TIMESTEP_COST = -0.05

    def cost(self, current_observation: Observation,
             historical_observations: List[Observation], step: int) -> float:
        previous_observation = historical_observations[-1]
        cost = step * self.TIMESTEP_COST

        player_stock_diff = previous_observation.player_stocks - \
            current_observation.player_stocks
        enemy_stock_diff = previous_observation.enemy_stocks - \
            current_observation.enemy_stocks
        player_life_diff = current_observation.player_percent - \
            previous_observation.player_percent
        enemy_life_diff = current_observation.enemy_percent - \
            previous_observation.enemy_percent

        cost += player_stock_diff * self.STOCK_LOSS_COST
        cost += player_life_diff * self.LIFE_LOSS_COST

        cost += enemy_stock_diff * self.STOCK_INFLICT_COST
        cost += enemy_life_diff * self.LIFE_INFLICT_COST

        return cost
