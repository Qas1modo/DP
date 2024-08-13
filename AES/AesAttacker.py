import numpy as np

from AES import AesConstants
from AES.Aes import Aes
from Helpers import hamming_weight


class AesAttacker:

    def __init__(self):
        self.aes = Aes()

    def attack(self, plain_text_field, traces):
        extracted_key = []
        for index in range(AesConstants.KEY_SIZE):
            for key_byte in range(AesConstants.BYTE_CONSTANT):
                theoretical_hamming_weights_byte = np.empty(AesConstants.TRACES)
                for x in range(AesConstants.TRACES):
                    plain_text_byte = plain_text_field[x][index]
                    theoretical_hamming_weights_byte[x] = hamming_weight(
                        int(self.aes.sbox[plain_text_byte ^ key_byte]))
                correlation = np.corrcoef(theoretical_hamming_weights_byte, traces[index])[0, 1]
                if correlation > AesConstants.CONFIDENCE_AES:
                    extracted_key.append(key_byte)
            if len(extracted_key) != index + 1:
                error = (f"Key not found (duplicate found) with {AesConstants.CONFIDENCE_AES}"
                         f" confidence, {AesConstants.TRACES}")
                raise Exception(error)
        return extracted_key
