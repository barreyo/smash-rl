"""The actual RL Agent"""

import logging
import os
from pathlib import Path

import numpy as np

from algorithms.dqn.dqn import DQN
from algorithms.e_greedy.e_greedy import EGreedy
from framework.agent import Agent
from framework.games.ssbm.ssbm_action import SSBMAction
from framework.games.ssbm.ssbm_action_space import SSBMActionSpace
from framework.games.ssbm.ssbm_observation import SSBMObservation

log = logging.getLogger(__name__)


class SSBMAgent(Agent):
    """DQNetwork implementation for SSBM."""

    def __init__(self, inference_only=False):
        super().__init__(SSBMActionSpace())
        self.inference_only = inference_only
        self.q = DQN(
            observation_size=SSBMObservation.size(),
            action_size=self.action_space.n_actions,
            learning_rate=0.01,
            gamma=0.9,
            batch_size=1
        )
        self.e_greedy = EGreedy()

    def act(self, observation: SSBMObservation, timestep: int) -> SSBMAction:
        if not self.inference_only and self.e_greedy.predict(timestep):
            return self.action_space.random_action()

        actions = self.q.predict(observation.as_array())
        best_action = np.argmax(actions)
        return SSBMAction.from_index(best_action)

    # TODO: Update learn to take in lists of everything for proper batching
    def learn(self, observation: SSBMObservation,
              observation_next: SSBMObservation, action: SSBMAction,
              reward: float, done: float):

        batched_observations = [observation]
        batched_observations_next = [observation_next]
        batched_actions = [action]

        observations = [o.as_array() for o in batched_observations]
        observations_next = [o.as_array() for o in batched_observations_next]
        actions = [a.as_array() for a in batched_actions]

        return self.q.train(observations, observations_next, actions, [reward], [done])

    def load(self, path='./trained_dqn/dqn.ckpt'):
        if not Path(os.path.dirname(path)).exists():
            log.info(
                f'No pre-trained agent found in {path}... Running new model')
            return

        self.q.load(path)

    def save(self, path='./trained_dqn/dqn.ckpt'):
        log.info('Saving agent...')
        return self.q.save(path)
