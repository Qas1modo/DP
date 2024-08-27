import itertools

from ASCON import AsconConstants
from ASCON.Ascon import Ascon
import numpy as np
from Helpers import get_bit_on_index
from Models.BestGuess import BestGuess


class AsconAttacker:

    def __init__(self, traces, nonces):
        self.simulated_traces = traces
        self.nonces = nonces
        self.current_nonce_m1 = 0
        self.current_nonce_m2 = 0
        self.x1_key = 0

    def attack_x1(self):
        for attack_index in range(36):  # 36 iterations are necessary to extract all key bits (x1)
            trace_for_attack = self.simulated_traces[attack_index]
            best_guess: BestGuess = BestGuess()
            for k0, k1, k2 in itertools.product(range(2), repeat=3):
                key_guess_bits = []
                for trace_index in range(AsconConstants.TRACES):
                    self.current_nonce_m1 = self.nonces[trace_index][0]
                    self.current_nonce_m2 = self.nonces[trace_index][1]
                    expected_bit = (self.get_part_s0(attack_index, 0, k0) ^
                                    self.get_part_s0(attack_index, 45, k1) ^
                                    self.get_part_s0(attack_index, 36, k2))
                    key_guess_bits.append(expected_bit)
                correlation: float = abs(np.corrcoef(trace_for_attack, key_guess_bits)[0, 1].item())
                if correlation > best_guess.correlation:
                    best_guess.update_guess(correlation, k0, k1, k2)
            self.x1_key += (best_guess.k0 << (AsconConstants.BIT_SIZE - attack_index - 1))
            if attack_index < 28:  # Use k2 for key extraction
                self.x1_key += (best_guess.k2 << (27 - attack_index))
        return self.x1_key

    def attack_x2(self):
        key = 0
        for attack_index in range(39):  # 39 iterations are necessary to extract all key bits (x2)
            trace_for_attack = self.simulated_traces[attack_index]
            best_guess: BestGuess = BestGuess()
            for k0, k1, k2 in itertools.product(range(2), repeat=3):
                key_guess_bits = []
                for trace_index in range(AsconConstants.TRACES):
                    self.current_nonce_m1 = self.nonces[trace_index][0]
                    self.current_nonce_m2 = self.nonces[trace_index][1]
                    expected_bit = (self.get_part_s1(attack_index, 0, k0) ^
                                    self.get_part_s1(attack_index, 3, k1) ^
                                    self.get_part_s1(attack_index, 25, k2))
                    key_guess_bits.append(expected_bit)
                correlation: float = abs(np.corrcoef(trace_for_attack, key_guess_bits)[0, 1].item())
                if correlation > best_guess.correlation:
                    best_guess.update_guess(correlation, k0, k1, k2)
            key += (best_guess.k2 << (38 - attack_index))
            if attack_index < 25:
                key += (best_guess.k0 << (AsconConstants.BIT_SIZE - attack_index - 1))
        return Ascon.reverse_round_key(0, key)

    def get_part_s0(self, attack_index: int, index: int, key_guess: int) -> int:
        current_index = (attack_index + index) % AsconConstants.BIT_SIZE
        x4_bit = get_bit_on_index(self.current_nonce_m2, current_index)
        x3_bit = get_bit_on_index(self.current_nonce_m1, current_index)
        return (key_guess & x4_bit) ^ x3_bit

    def get_part_s1(self, attack_index: int, index: int, key_guess: int) -> int:
        current_index = (attack_index + index) % AsconConstants.BIT_SIZE
        x3_bit = get_bit_on_index(self.current_nonce_m1, current_index)
        x4_bit = get_bit_on_index(self.current_nonce_m2, current_index)
        x1_bit = get_bit_on_index(self.x1_key, current_index)
        return (x3_bit & key_guess ^ x3_bit & x1_bit ^ x3_bit) ^ x4_bit
