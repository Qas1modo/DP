class Ascon:

    @staticmethod
    def add_round_key(current_round, s):
        s[2] ^= (0xf0 - current_round * 0x10 + current_round * 0x1)

    @staticmethod
    def reverse_round_key(current_round, key):
        key ^= (0xf0 - current_round * 0x10 + current_round * 0x1)
        return key

    @staticmethod
    def compute_substitution(S):
        S[0] ^= S[4]
        S[4] ^= S[3]
        S[2] ^= S[1]
        T = [(S[i] ^ 0xFFFFFFFFFFFFFFFF) & S[(i + 1) % 5] for i in range(5)]
        for i in range(5):
            S[i] ^= T[(i + 1) % 5]
        S[1] ^= S[0]
        S[0] ^= S[4]
        S[3] ^= S[2]
        S[2] ^= 0XFFFFFFFFFFFFFFFF

    @staticmethod
    def compute_diffusion_layer(S):
        S[0] ^= Ascon.rotr(S[0], 19) ^ Ascon.rotr(S[0], 28)
        S[1] ^= Ascon.rotr(S[1], 61) ^ Ascon.rotr(S[1], 39)
        S[2] ^= Ascon.rotr(S[2], 1) ^ Ascon.rotr(S[2], 6)
        S[3] ^= Ascon.rotr(S[3], 10) ^ Ascon.rotr(S[3], 17)
        S[4] ^= Ascon.rotr(S[4], 7) ^ Ascon.rotr(S[4], 41)

    @staticmethod
    def rotr(val, r):
        return (val >> r) | ((val & (1 << r) - 1) << (64 - r))