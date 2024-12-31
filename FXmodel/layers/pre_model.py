
import tensorflow as tf

from FXmodel.layers.embedding import *
from FXmodel.layers.attention import *

def flow_model(config, block_count,
               use_causal_mask):

  return Sequential([
      tf.keras.Input(shape=(None, config.d_model,)),

      Sequential([
          Blocks(config, use_causal_mask)
            for _ in range(block_count)
      ])
  ])