
from FXmodel.configurations.config_low_high import ConfigLowHigh
from FXmodel.configurations.config_close import ConfigClose

from FXmodel.layers.pre_model import *
from FXmodel.layers.attention import *
from FXmodel.layers.linear import *
from FXmodel.layers.concat_linear import *

from tensorflow.keras import Model

class Low_Model:

    def __init__(self):
        
        '''
        this Low model is init only once thru out runtime (it builds the model only once),
        but prediction can be called anytime
        '''
        self.model = None
        self.model_path = "./FXmodel/weights/EURUSD_Low.weights.h5"
        self.__build_model()

    def __build_model(self):
        '''
        Only build model when model is not found in controller
        '''
        
        inputs = tf.keras.Input(shape=(None,))

        def split_tensor(x):
            # This can be any TensorFlow logic you want
            return tf.split(x, num_or_size_splits=3, axis=-1)

        low, high, close = layers.Lambda(split_tensor)(inputs)

        embedded_low = Embedding(ConfigLowHigh())(low)
        output_low = flow_model(config=ConfigLowHigh(),
                            block_count=2,
                            use_causal_mask=True)(embedded_low)

        #For high
        embedded_high = Embedding(ConfigLowHigh())(high)
        output_high = flow_model(config=ConfigLowHigh(),
                                block_count=2,
                                use_causal_mask=False)(embedded_high)

        #for close
        embedded_close = Embedding(ConfigClose())(close)
        output_close = flow_model(config=ConfigClose(),
                                block_count=2,
                                use_causal_mask=False)(embedded_close)

        #Mix low, high and close together
        high_close_mix = ConcatAndLinear(ConfigLowHigh())(output_high, output_close)

        cross_attention = Blocks(config=ConfigLowHigh(),
                                causal_mask=False)(output_low, high_close_mix)

        flows = flow_model(config=ConfigLowHigh(),
                        block_count=4,
                        use_causal_mask=True)(cross_attention)

        outputs = Linear(ConfigLowHigh())(flows)

        self.model = Model(inputs, outputs)
        
        #Loads weights from pretrained weights
        self.model.load_weights(self.model_path)


    def predict(self, **kwargs):
        '''
        Receives any size of input and return only 1 value of type integer
        '''
        re_low = kwargs['re_low']
        re_high = kwargs['re_high']
        re_close = kwargs['re_close']

        X = np.concatenate((re_low, re_high, re_close), axis=-1).reshape(1, -1)

        m = len(re_low)

        pe = Get_Position(m, ConfigLowHigh.d_model)

        low, high, close = self.model.layers[1](X)

        print(high)

        embedded_high = self.model.layers[2](high)
        output_high = self.model.layers[5](embedded_high + pe)

        embedded_close = self.model.layers[3](close)
        output_close = self.model.layers[6](embedded_close + pe)

        embedded_low = self.model.layers[4](low)
        output_low = self.model.layers[7](embedded_low + pe)

        high_close_mix = self.model.layers[8](output_high, output_close)

        cross_attention = self.model.layers[9](output_low, high_close_mix)

        flows = self.model.layers[10](cross_attention)

        logits = self.model.layers[11](flows)

        prediction = np.argmax(logits[:,-1, :][0], axis=-1)

        return prediction.astype('int8')
    

