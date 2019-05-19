
from typing import List

import tensorflow as tf

from framework.action import Action
from framework.observation import Observation
from framework.reward import Reward


class DQN():

    def __init__(self, observation_size: int, action_size: int,
                 learning_rate: float, gamma: float, batch_size: int = 32,
                 name: str = 'DQNetwork'):
        self.session = tf.Session()
        self.observation_size = observation_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.gamma = gamma

        self.hidden_layers = [128, 128, 64]

        # TF placeholders
        self.observations = tf.placeholder(tf.float32,
                                           shape=[self.batch_size,
                                                  observation_size],
                                           name="observations")
        self.observations_next = tf.placeholder(tf.float32,
                                                shape=[self.batch_size,
                                                       observation_size],
                                                name="observations_next")
        self.actions = tf.placeholder(tf.float32,
                                      shape=(self.batch_size, self.action_size),
                                      name="actions")
        # AKA Q(a', s')
        self.rewards = tf.placeholder(tf.float32,
                                      shape=(self.batch_size,),
                                      name="rewards")
        self.done_flags = tf.placeholder(tf.float32,
                                         shape=(self.batch_size,),
                                         name="done_flags")

        self.q_network = self._build_dense_network(self.observations,
                                                   self.hidden_layers,
                                                   'DQN_Network')

        self.target_q_network = self._build_dense_network(
            self.observations_next, self.hidden_layers, 'target_DQN_Network')

        # action_one_hot = tf.one_hot(
        #     self.actions, self.action_size, 1.0, 0.0, name='action_one_hot')
        prediction = tf.reduce_sum(
            self.q_network * self.actions, reduction_indices=-1,
            name='q_acted')

        max_q_prim = tf.reduce_max(self.target_q_network, axis=-1)
        y = self.rewards + (1.0 - self.done_flags) * self.gamma * max_q_prim

        self.loss = tf.reduce_mean(
            tf.square(prediction - tf.stop_gradient(y)), name='loss_mse_train')
        self.optimizer = tf.train.RMSPropOptimizer(
            self.learning_rate).minimize(self.loss)

        init = tf.initializers.global_variables()
        self.session.run(init)

    def _build_dense_network(self, inputs, hidden_layers, network_name):
        initializer = tf.contrib.layers.xavier_initializer()

        with tf.variable_scope(network_name):
            for i, size in enumerate(hidden_layers):
                inputs = tf.layers.dense(
                    inputs,
                    size,
                    activation=tf.nn.relu,
                    kernel_initializer=initializer,
                    name=f"{network_name}_l_{i}"
                )
        output = tf.layers.dense(
            inputs, self.action_size, activation=None,
            kernel_initializer=initializer, name=f"{network_name}_output")

        return output

    def predict(self, observations: Observation) -> Action:
        pass

    def train(self, observations: List[List[float]],
              observations_next: List[List[float]], actions: List[List[float]],
              rewards: List[float], done_flags: List[float]) -> float:

        feed_dict = {
            self.observations: observations,
            self.actions: actions,
            self.rewards: rewards,
            self.observations_next: observations_next,
            self.done_flags: done_flags,
        }
        _, _, _, loss = self.session.run(
            [self.optimizer, self.q_network,
             self.target_q_network, self.loss],
            feed_dict=feed_dict)
        return loss
