
import tensorflow as tf
from tensorflow.keras import layers, Sequential
from tensorflow.keras.layers import Layer


class ConcatAndLinear(Layer):

    def __init__(self, config):

        super().__init__()

        self.ffn = Sequential([

            layers.Dense(config.hidden_unit, activation = 'gelu'),

            layers.Dropout(config.drop_out_rate),

            layers.Dense(config.d_model),

            layers.Dropout(config.drop_out_rate)

        ])

        self.layernorm = layers.LayerNormalization()

        self.add = layers.Add()

    def call(self, inputs1, inputs2):
        Z = tf.concat([inputs1, inputs2], axis=1)

        x = self.ffn(Z)

        x = self.add([x, Z])

        return self.layernorm(x)