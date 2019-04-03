import tensorflow as tf


class DQN():

    def __init__(self, observation_size, action_size,
                learning_rate, name='DQNetwork'):

        self.observation_size = observation_size
        self.action_size = action_size
        self.learning_rate = learning_rate

        self.hidden_layers = [128, 128, 64]

        # TF placeholders
        self.observations = tf.placeholder(tf.float32, [None, observation_size], name="observations")
        self.actions = tf.placeholder(tf.float32, [None, action_size], name="actions")
        self.target_Q = tf.placeholder(tf.float32, [None, action_size], name="target_Q")

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

        self.output = tf.layers.dense(inputs, self.action_size,
            activation=None, kernel_initializer=initializer, name="output")

        # Calculate Q value, from network output, multiplied by curent action, and get the
        # maximum value (using reduce_sum)
        self.Q = tf.reduce_sum(tf.multiply(self.output, self.actions), axis=1)

        self.loss = tf.reduce_mean(tf.square(self.target_Q - self.Q))
        self.optimizer = tf.train.RMSPropOptimizer(self.learning_rate).minimize(self.loss)


    def predict(self, observation):
        pass

    def train(self, observation, action, reward) -> float:
        # return loss
        pass
