
import random
from collections import deque
from typing import Any, Iterable, List, Text

import numpy as np
import tensorflow as tf
from tensorflow import keras


class DQNv2():

    def __init__(self, observation_size: int, action_size: int,
                 learning_rate: float, gamma: float, batch_size: int = 32,
                 name: Text = 'DQNetwork'):
        self.session = tf.compat.v1.Session()
        self.observation_size = observation_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.gamma = gamma

        self.hidden_layers = [128, 256, 128]
        self.memory = deque(maxlen=200)  # type: Iterable[Any]
        self.model = self.__build_model()

    def __build_model(self):
        model = keras.Sequential()

        # Input layer
        model.add(keras.layers.Dense(
            32, input_dim=self.observation_size,
            activation='relu'))

        # Hidden layers
        for size in self.hidden_layers:
            model.add(keras.layers.Dense(size, activation='relu'))

        # Output layer
        model.add(keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(
            lr=self.learning_rate))

        return model

    def __memorize(
            self, observation: List[float], action: List[float],
            reward: float, next_observation: List[float],
            done: bool) -> None:
        self.memory.append(
            (observation, action, reward, next_observation, done))

    def __replay(self, batch_size: int) -> float:

        def fit(o, a, r, no, done):
            target = r
            if not done:
                target = (r + self.gamma * np.amax(self.model.predict(
                    np.reshape(no, [1, self.observation_size]))[0]))

            o = np.reshape(o, [1, self.observation_size])
            target_f = self.model.predict(o)
            target_f[0][a] = target
            return self.model.fit(o, target_f, epochs=1, verbose=0)

        if len(self.memory) < batch_size:
            o, a, r, no, done = self.memory[-1]
            res = fit(o, a, r, no, done)
            return np.average(res.history['loss'])

        mini_batch = random.sample(self.memory, batch_size)
        histories = list()  # type: List[keras.History]

        for o, a, r, no, done in mini_batch:
            res = fit(o, a, r, no, done)
            histories.append(res)

        return np.average([np.average(v.history['loss']) for v in histories])

    def predict(self, observation: List[float]):
        predictions = self.model.predict(observation)
        return np.argmax(predictions[0])

    def train(self, observations: List[List[float]],
              observations_next: List[List[float]], actions: List[List[float]],
              rewards: List[float], done_flags: List[float]) -> float:

        self.__memorize(observations[0], actions[0],
                        rewards[0], observations_next[0], bool(done_flags[0]))
        avg_loss = self.__replay(self.batch_size)
        return avg_loss

    def save(self, path: Text):
        self.model.save_weights(path)
        return path

    def load(self, path: Text):
        self.model.load_weights(path)
