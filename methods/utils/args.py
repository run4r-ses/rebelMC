import pickle
import base64

def encode_args(config, log_path):
    return base64.b64encode(pickle.dumps((config, log_path))).decode()

def decode_args(encoded):
    return pickle.loads(base64.b64decode(encoded))
