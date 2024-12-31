
from tensorflow.keras import layers, Sequential
from tensorflow.keras.layers import Layer

class Blocks(Layer):
    def __init__(self, config, causal_mask):

        super().__init__()

        self.mha = layers.MultiHeadAttention(num_heads=config.num_heads,
                                             key_dim = config.d_model)
        self.ffn = Sequential([

            layers.Dense(config.hidden_unit, activation = 'gelu'),

            layers.Dropout(config.drop_out_rate),

            layers.Dense(config.d_model),

            layers.Dropout(config.drop_out_rate)

        ])
        self.use_causal_mask = causal_mask

        self.layernorm = layers.LayerNormalization()

        self.add = layers.Add()


    def call(self, inputs, inputs_cross=None):
        if (inputs_cross == None):
          inputs_cross = inputs

        attention_output = self.mha(
            query = inputs,
            key = inputs_cross,
            value = inputs_cross,
            use_causal_mask = self.use_causal_mask,
        )

        x = self.add([inputs, attention_output])

        inputs2 = self.layernorm(x)

        ##Feed Forward
        x = self.ffn(inputs2)

        x = self.add([x, inputs2])

        return self.layernorm(x)