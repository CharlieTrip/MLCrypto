import os, glob, sys
import pandas as pd
from colorama import Fore
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sklearn import metrics

class Classifiers(object):
    """docstring for MLClustering."""

    def __init__(self, alg_training_set, experiments=1, trials=1, training_size=31250, target_sizes=[31250]):
        self.alg_training_set = alg_training_set
        self.experiments = experiments
        self.trials = trials
        self.training_size = training_size
        self.target_sizes = target_sizes

        self.targetList = self.__loadTargetDatasetList(alg_training_set,trials,target_sizes)
        self.training = self.__loadTrainingDataset()


    def __loadTrainingDataset(self):
        files = []
        prefix = "trainingDatasets/"
        for alg_trainig in self.alg_training_set:
            directory = prefix + alg_trainig +"_"+ str(self.experiments) +".gzip"
            files = files + glob.glob(directory)

        if files:
            df = pd.DataFrame(columns=['algorithm', 'entropy', 'nonce', 'output'])
            for filename in files:
                df_training = pd.read_parquet(filename, columns=None)
                df = df.append(df_training.sample(n=self.training_size).reset_index(drop=True))
            return df
        
        else:
            print('{}ERROR: Please, run generateTrainingDatasets.py to generate the training datasets{}'.format(
                Fore.RED,Fore.RESET
            ))

    def __loadTargetDataset(self,alg,trial):
        target_filename = 'targetDatasets/{}_{}.gzip'.format(alg,trial)
        if os.path.isfile(target_filename):
            data = pd.read_parquet(target_filename, columns=None)
        else:
            print('{}ERROR: Please, run generate the correct target dataset: {}{}'.format(
                Fore.RED, target_filename,Fore.RESET
            ))
            data = False
        return data

    def __loadTargetDatasetList(self,alg_training_set,trials,sizes):
        target_list = []
        for k in sizes:
            tmp = []
            for trial in range(trials):
                target1 = self.__loadTargetDataset(alg_training_set[0],trial)
                target2 = self.__loadTargetDataset(alg_training_set[1],trial)
                target1 = target1.head(n=k)
                target2 = target2.head(n=k)
                target = pd.concat([target1, target2], ignore_index=True)
                tmp.append(target)
            target_list.append(tmp)
        return target_list



    def bayes(self):
        from sklearn.naive_bayes import GaussianNB

        X = self.training.drop(['algorithm','entropy','nonce'], axis=1)
        Y = self.training['algorithm']

        # Instantiate the classifier
        gnb = GaussianNB()
        # Train classifier
        gnb.fit(X, Y)
        
        accuracies = []

        for target_size in self.targetList:
            accuracy = []
            for tar in target_size:
                X_test = tar.drop(['algorithm','entropy','nonce'], axis=1)
                Y_test = tar['algorithm']
                y_pred = gnb.predict(X_test)
                accuracy += [ metrics.accuracy_score(Y_test, y_pred) ]
            accuracies += [accuracy]
        return accuracies


if __name__ == "__main__":
    alg_list = ['tdea', 'aes128', 'aes192', 'aes256', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha1hmac',
           'sha224hmac', 'sha256hmac', 'sha384hmac','sha512hmac']
    for alg in alg_list:
        print('{}Naive Bayes for: {}{}'.format(Fore.BLUE, alg, Fore.RESET))
        svm_cluster = Classifiers(alg)
        svm_cluster.bayes()
        print('{}Random Forest for: {}{}'.format(Fore.BLUE, alg, Fore.RESET))
        svm_cluster.rf()
        del svm_cluster
        print()
