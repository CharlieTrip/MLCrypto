import pandas as pd
import os, copy
from colorama import Fore
from add_data import generate_drbg
from tqdm import tqdm
from itertools import combinations
from ml.classifiers import Classifiers
from datetime import date


# ---------------------- 
#           Modify these values with your own values

# Experiment: # Training Dataset
EXPERIMENTS = 2**10
# Trials: # Target Dataset
TRIALS = 1
# Training's Datasets Size
TRAINING_SIZE = [2**i for i in range(12,13)]
# Target's Datasets Size
TARGET_SIZE = [2**i for i in range(15,16)]


# ---------------------- 

LENGTH_TRAINING_DATASET = 100

def generate_new_data(combination, experiment, size, dest):
    for alg in combination:
        filename = "{}/{}_{}.gzip".format(dest, alg, experiment)
        
        if os.path.isfile(filename):
            os.remove(filename)
        
        if not os.path.isfile(filename):
            aux = 0
            while aux < LENGTH_TRAINING_DATASET:
                output, entropy, nonce = generate_drbg(alg,size=size)
                tmp = {}
                for cont, y in enumerate(output):
                    tmp[cont] = {'algorithm': alg, "entropy": entropy,
                              "nonce": nonce, "output": int.from_bytes(y, "big")}

                df = pd.DataFrame.from_dict(tmp, "index")
                aux += len(output)

            df.to_parquet(filename)


def menu(ori_alg_list):
    cad = ''
    for cont in range(len(ori_alg_list)):
        cad += '({}){}  '.format(cont, ori_alg_list[cont])
    
    print(cad)
    print('Introduce the number of algorithms to be used (separated by , ) ')
    choice1 = input('Leave it blank to use them all: ')
    
    try:
        choice1 = choice1.split(',')
        alg_list = []
        for elem in choice1:
            alg_list.append(ori_alg_list[int(elem)])
    except:
        alg_list = copy.deepcopy(ori_alg_list)

    # while True:
    #     print('(1) Naive Bayes; (2) Random Forest; (3) Both')
    #     option = int(input('Introduce the number of ML algorithm to execute: '))
    #     if 0<option<4:
    #         break
    option = 1
        
    return alg_list, option

def generate_folders(folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)

def main():
    folders = ['targetDatasets', 'trainingDatasets', 'experiments_cvs']
    ori_alg_list = ['tdea', 'aes128', 'aes192', 'aes256', 'sha1', 'sha224', 'sha256', 'sha384',
                'sha512', 'sha1hmac', 'sha224hmac', 'sha256hmac', 'sha384hmac','sha512hmac']


    # Generic sparse choice: 0,3,6,11
    alg_list, option = menu(ori_alg_list)
    for folder in folders:
        generate_folders(folder)

    
    # All the combination to train and check
    comb = list(combinations(alg_list, 2))
    datapoint, j = ({},0)
    
    print('{}Generating Target Dataset{}'.format(Fore.BLUE,Fore.RESET))
    for cont in range(TRIALS):
        generate_new_data(alg_list, cont, max(TARGET_SIZE), "targetDatasets")

    print('{}Running Experiments{}'.format(Fore.BLUE, Fore.RESET))
    for cont in tqdm(range(EXPERIMENTS)):
        generate_new_data(alg_list, cont, max(TRAINING_SIZE), "trainingDatasets")
        
        for lt in TRAINING_SIZE:
            
            for combination in comb:
                
                svm_cluster = Classifiers(combination, cont, TRIALS,
                                                training_size=lt,target_sizes=TARGET_SIZE)
                
                if option in [1,3]:
                    result_bayes = svm_cluster.bayes() # [0.5]*TRIALS
                    if not result_bayes:
                        result_bayes = [[None]*TRIALS]*len(TARGET_SIZE)
                else:
                    result_bayes = [[None]*TRIALS]*len(TARGET_SIZE)
                    
                del svm_cluster

                for st in range(len(TARGET_SIZE)):
                    for trial in range(TRIALS):
                        datapoint[j] = {'training': cont, 'target': trial, 'algs': combination,
                                        'NB': result_bayes[st][trial], 'trainsize': lt, 'targetsize': TARGET_SIZE[st]}
                        j = j+1


    df = pd.DataFrame.from_dict(datapoint, "index")
    filename = "experiments_cvs/CSV_" + date.today().strftime("%Y_%m_%d") + ".csv"
    df.to_csv(filename, encoding='utf-8')




if __name__ == "__main__":
    main()
