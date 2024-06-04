from colorama import Fore
from tqdm import tqdm
from algorithms import drbg
import binascii


def generate_drbg(alg='sha512', insert=False, entropy=False, nonce=False,verbose=False, size=31250):
    '''
    Generate random values using the function given by alg parameter. If we want to generate the same output
    we have to provide both entropy and nonces values. Otherwise this function will generate random values

    :param alg: name of the family to generate random values
    :param insert: parameter that indicates whether to store or not values into de db
    :param entropy: fixed entropy
    :param nonce:  fixed nonce
    '''
    getattr(tqdm, '_instances', {}).clear()
    
    # Verbosity trick
    vprint = print if verbose else lambda *a, **k: None

    obj, nonce, entropy = drbg.new(alg, nonce, entropy)
    vprint('{}Nonce: {}{}'.format(Fore.LIGHTMAGENTA_EX,nonce,Fore.RESET))
    vprint('{}Entropy: {}{}'.format(Fore.LIGHTMAGENTA_EX,entropy,Fore.RESET))
    output = []

    for count in range(size):
        aux = binascii.hexlify(obj.generate(4))
        if insert:
            aux = int.from_bytes(aux, "big")
        vprint(aux)
        output.append(aux)

    return output, entropy, nonce


if __name__ == "__main__":
    alg_list = ['tdea', 'aes128', 'aes192', 'aes256', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha1hmac',
           'sha224hmac', 'sha256hmac', 'sha384hmac','sha512hmac']

    for alg in alg_list:
        print('{}Generating random numbers for: {}{}'.format(Fore.BLUE,alg,Fore.RESET))
        output, entropy, nonce = generate_drbg(alg)
