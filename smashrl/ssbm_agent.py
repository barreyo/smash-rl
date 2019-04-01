"""The actual RL Agent"""

import numpy as np

from algorithms.dqn.dqn import DQN
from algorithms.e_greedy.e_egreedy import EGreedy
from framework.agent import Agent
from framework.games.ssbm.ssbm_action import SSBMAction
from framework.games.ssbm.ssbm_action_space import SSBMActionSpace
from framework.games.ssbm.ssbm_observation import SSBMObservation


class SSBMAgent(Agent):
    """DQNetwork implementation for SSBM."""

    def __init__(self):
        super().__init__(SSBMActionSpace())
        # TODO: xd
        self.q = DQN(learning_rate=1.0)
        self.e_greedy = EGreedy()

    def act(self, observation: SSBMObservation, timestep: int) -> SSBMAction:
        if self.e_greedy.predict(timestep):
            return np.choice(self.action_space.random_action())

        actions = self.algorithm.predict(observation.get_np())
        best_action = np.argmax(actions)
        return self.action_space.action_to_index(best_action)

    def learn(self, observation: SSBMObservation, action: SSBMAction,
              reward: float):

        self.q.train(observation.as_array(), action.get_index(), reward)

    def load(self):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()
