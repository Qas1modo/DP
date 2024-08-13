import math
from random import random

from ASCON import AsconConstants
from Helpers import generate_random_number
from ASCON.Ascon import Ascon
import numpy as np


class AsconHelper:

    def __init__(self):
        self.nonces = []
        self.traces = []

    def calculate_internal_state(self):
        key_x1 = AsconConstants.KEY[0]
        key_x2 = AsconConstants.KEY[1]
        nonce_x3 = generate_random_number()
        nonce_x4 = generate_random_number()
        s = [AsconConstants.IV, key_x1, key_x2, nonce_x3, nonce_x4]
        self.nonces.append([nonce_x3, nonce_x4])
        Ascon.add_round_key(0, s)
        Ascon.compute_substitution(s)
        Ascon.compute_diffusion_layer(s)
        return s

    def create_simulated_traces(self):
        simulated_traces = []
        for i in range(AsconConstants.TRACES):
            s = self.calculate_internal_state()
            trace_for_single_state = []
            for col in range(64):
                result = AsconConstants.CONSTANT_NOISE + math.floor(AsconConstants.VARIABLE_NOISE * random())
                for row in range(5):  # Will update to capture 64 bit register -> currently ASCON column
                    result += s[row] & 0x01
                    s[row] >>= 1
                trace_for_single_state.append(result)
            trace_for_single_state.reverse()
            simulated_traces.append(trace_for_single_state)
        return np.array(simulated_traces).T.tolist()  # Make rows to contain traces for specific column
