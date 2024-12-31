
from tensorflow.keras import layers
from tensorflow.keras.layers import Layer
import numpy as np

class Embedding(Layer):
    def __init__(self, config):
        super().__init__()

        self.embed = layers.Embedding(config.vocab_size, config.d_model)

    def call(self, inputs):
        return self.embed(inputs)
    

def Get_Position(context_length, d_model, n=10000):
    P = np.zeros((context_length ,d_model))
    for k in range(context_length):
        for i in np.arange(int(d_model/2)):
            denominator = np.power(n, 2*i/d_model)
            P[k, 2*i] = np.sin(k/denominator)
            P[k, 2*i + 1] = np.cos(k/denominator)

    return P