from AES import AesConstants
from AES.AesAttacker import AesAttacker
from AES.AesHelper import AesHelper
from ASCON.AsconHelper import AsconHelper

from Helpers import generate_random_array

from ASCON.AsconAttacker import AsconAttacker


def main():
    print("AES")
    plain_text_field = generate_random_array(AesConstants.TRACES, AesConstants.ROW_SIZE,
                                             AesConstants.BYTE_CONSTANT)
    aes_helper = AesHelper()
    aes_simulated_traces = aes_helper.calculate_simulated_traces(plain_text_field, AesConstants.KEY)
    aes_attacker = AesAttacker()
    print("key:", aes_attacker.attack(plain_text_field, aes_simulated_traces.transpose()))
    print("\nASCON")
    ascon_helper = AsconHelper()
    simulated_traces = ascon_helper.create_simulated_traces()
    nonces = ascon_helper.nonces
    ascon_attacker = AsconAttacker(simulated_traces, nonces)
    print("x1:", hex(ascon_attacker.attack_x1()))
    print("x2:", hex(ascon_attacker.attack_x2()))


if __name__ == '__main__':
    main()
