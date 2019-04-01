import tensorflow as tf


class DQN():

    def __init__(self, observation_size, action_size,
                learning_rate, name='DQNetwork'):

        self.observation_size = observation_size
        self.action_size = action_size
        self.learning_rate = learning_rate

        self.hidden_layers = [128, 128, 64]
        self.observations = tf.placeholder(tf.float32, [None, observation_size], name="observations")

        inputs = self.observations
        initializer = tf.contrib.layers.xavier_initializer()

        with tf.variable_scope(name):
            for i, size in enumerate(self.hidden_layers):
                inputs = tf.layers.dense(
                    inputs,
                    size,
                    activation=tf.nn.relu,
                    kernel_initializer=initializer,
                    name=f"{name}_l_{i}"
                )

        self.target = tf.layers.dense(inputs, self.action_size,
            activation=None, kernel_initializer=initializer, name="target")


    def predict(self, observation):
        pass

    def train(self, observation, action, reward) -> float:
        # return loss
        pass
