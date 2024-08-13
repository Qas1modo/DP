import math
from random import random

from AES import AesConstants
from AES.Aes import Aes
from Helpers import hamming_weight
import numpy as np


class AesHelper:

    def __init__(self):
        self.aes = Aes()

    def calculate_simulated_traces_byte(self, plain_text, key):
        result = []
        for key_byte, text_byte in zip(key, plain_text):
            internal_state = hamming_weight(self.aes.sbox[key_byte ^ text_byte])
            noised_internal_state = (internal_state + math.floor(AesConstants.NOISE * random())
                                     + AesConstants.CONSTANT_NOISE)
            result.append(noised_internal_state)
        return result

    def calculate_simulated_traces(self, plain_text_field, key):
        result = []
        for plain_text_byte in plain_text_field:
            result.append(self.calculate_simulated_traces_byte(plain_text_byte, key))
        return np.array(result)
