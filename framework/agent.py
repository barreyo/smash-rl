
from framework.action import Action
from framework.action_space import ActionSpace
from framework.observation import Observation


class Agent():

    def __init__(self, action_space: ActionSpace):
        self.action_space = action_space

    def act(self, observation: Observation) -> Action:
        raise NotImplementedError()

    def learn(self, observation: Observation, action: Action,
              reward: float) -> None:
        raise NotImplementedError()

    def load(self):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()
