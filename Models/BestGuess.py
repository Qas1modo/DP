class BestGuess:
    correlation = 0
    k0 = 0
    k1 = 0
    k2 = 0

    def update_guess(self, correlation: float, key_bit_k0: int, key_bit_k1: int, key_bit_k2: int):
        self.correlation = correlation
        self.k0 = key_bit_k0
        self.k1 = key_bit_k1
        self.k2 = key_bit_k2
