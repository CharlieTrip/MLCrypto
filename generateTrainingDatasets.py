import pandas as pd
import os
from colorama import Fore
from add_data import generate_drbg
from tqdm import tqdm

LENGTH_TRAINING_DATASET = 100
EXPERIMENTS = 1

if __name__ == "__main__":
    alg_list = ['tdea', 'aes128', 'aes192', 'aes256', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha1hmac',
                'sha224hmac', 'sha256hmac', 'sha384hmac' ,'sha512hmac']
    for experiment in range(1,EXPERIMENTS+1):
        for alg in alg_list:
            print('{}Generating random numbers for: {}{}'.format(Fore.BLUE ,alg ,Fore.RESET))
            filename = "tmp/trainingSet_{}_{}.gzip".format(alg,experiment)
            # filename = "targetDatasets/trainingSet_{}_{}.gzip".format(alg,experiment)
            
            if not os.path.isfile(filename):
                # df = pd.DataFrame(columns=['algorithm', 'entropy', 'nonce', 'output'])
                aux = 0
                while aux < LENGTH_TRAINING_DATASET:
                    output, entropy, nonce = generate_drbg(alg)
                    tmp = {}; i = 0
                    for y in tqdm(output):
                        tmp[i] = {'algorithm': alg, "entropy" :entropy,
                                        "nonce" :nonce,"output" :int.from_bytes(y,"big")}
                        i = i + 1
                    
                    df = pd.DataFrame.from_dict(tmp,"index")
                    aux += len(output)
                
                df.to_parquet(filename)