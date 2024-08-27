from typing import Tuple

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
            best_guess: Tuple[float, int] = (0, 0x00)
            for key_byte in range(AesConstants.BYTE_CONSTANT):
                theoretical_hamming_weights_byte = np.empty(AesConstants.TRACES)
                for x in range(AesConstants.TRACES):
                    plain_text_byte = plain_text_field[x][index]
                    theoretical_hamming_weights_byte[x] = hamming_weight(
                        int(self.aes.sbox[plain_text_byte ^ key_byte]))
                correlation = abs(np.corrcoef(theoretical_hamming_weights_byte, traces[index])[0, 1].item())
                if correlation > best_guess[0]:
                    best_guess = (correlation, key_byte)
            extracted_key.append(best_guess[1])
        return extracted_key
