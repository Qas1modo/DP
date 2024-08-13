import random
import numpy as np
import math
import Constants
from ASCON import AsconConstants


def hamming_weight(n: int) -> int:
    c = 0
    while n:
        c += 1
        n &= n - 1
    return c


def generate_random_array(x: int, y: int, limit: int) -> np.array:
    array = np.random.rand(x, y) * limit
    vfunc = np.vectorize(math.floor)
    return vfunc(array)


def generate_random_number(limit: int = Constants.INT_64) -> int:
    return random.randint(0, limit)


def get_bit_on_index(number: int, index: int, length: int = AsconConstants.BIT_SIZE) -> int:
    return number >> (length - index - 1) & 0x01
