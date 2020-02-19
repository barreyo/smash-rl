
import numpy as np


class EGreedy():

    def __init__(self, decay_rate: float = 0.01, explore_min: float = 0.01,
                 explore_max: float = 1.0):
        self.decay_rate = decay_rate
        self.explore_min = explore_min
        self.explore_max = explore_max

    def predict(self, timestep: int) -> bool:
        """
        Calculate if exploration should happening.

        Arguments:
        timestep -- Current simulation timestep as int

        Returns:
        True if should explore; else false

        """
        tradeoff = np.random.rand()
        explore_prob = self.explore_min + \
            (self.explore_max - self.explore_min) * \
            np.exp(-self.decay_rate * float(timestep))
        print(f'Explore prob: {explore_prob}')
        return explore_prob > tradeoff
