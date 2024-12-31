
class ConfigClose():
    vocab_size:int = 5 #There are 3001 possible values for CLOSE if contrained to [-150, 150] -> eos token is 3001
    d_model: int = 32
    hidden_unit: int = 128
    num_heads: int = 6
    drop_out_rate = 0.2