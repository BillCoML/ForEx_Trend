
class ConfigLowHigh():
    vocab_size:int = 3 #There are 1501 possible values for LOW and HIGH if contrained to [-150, 0] and [0,150], respectively. And EOS token is 1501
    d_model: int = 32
    hidden_unit: int = 128
    num_heads: int = 6
    drop_out_rate = 0.2