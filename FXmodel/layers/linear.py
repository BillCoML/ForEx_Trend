
from tensorflow.keras import layers
from tensorflow.keras.layers import Layer

class Linear(Layer):

    def __init__(self, config):

        super().__init__()
        self.linear = layers.Dense(config.vocab_size)

    def call(self, inputs):

        return self.linear(inputs)