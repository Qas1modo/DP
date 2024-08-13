import numpy as np


class Aes:

    def __init__(self):
        self.sbox = self.initialize_aes_sbox()

    @staticmethod
    def rotl8(x, shift):
        return ((x << shift) | (x >> (8 - shift))) & 0xFF

    def initialize_aes_sbox(self):
        sbox = [0] * 256
        p = 1
        q = 1

        while True:
            # multiply p by 3
            p = p ^ (p << 1) ^ (0x1B if p & 0x80 else 0)
            p &= 0xFF
            # divide q by 3 (equals multiplication by 0xf6)
            q ^= q << 1
            q ^= q << 2
            q ^= q << 4
            q ^= (0x09 if q & 0x80 else 0)
            q &= 0xFF
            # compute the affine transformation
            xformed = q ^ self.rotl8(q, 1) ^ self.rotl8(q, 2) ^ self.rotl8(q, 3) ^ self.rotl8(q, 4)
            sbox[p] = xformed ^ 0x63
            if p == 1:
                break

        # 0 is a special case since it has no inverse
        sbox[0] = 0x63
        return np.array(sbox)
