"""The actual RL Agent"""

from algorithms.dqn.dqn import DQN
from algorithms.e_greedy.e_greedy import EGreedy
from framework.agent import Agent
from framework.games.ssbm.ssbm_action import SSBMAction
from framework.games.ssbm.ssbm_action_space import SSBMActionSpace
from framework.games.ssbm.ssbm_observation import SSBMObservation


class SSBMAgent(Agent):
    """DQNetwork implementation for SSBM."""

    def __init__(self):
        super().__init__(SSBMActionSpace())
        self.q = DQN(
            observation_size=SSBMObservation.size(),
            action_size=self.action_space.n_actions,
            learning_rate=0.001,
            gamma=0.1,
            batch_size=1
        )
        self.e_greedy = EGreedy()

    def act(self, observation: SSBMObservation, timestep: int) -> SSBMAction:
        if self.e_greedy.predict(timestep):
            return self.action_space.random_action()

        action = self.q.predict(observation.get_np())
        return self.action_space.action_to_index(action)

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

    def load(self):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()
