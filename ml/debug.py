import os
import pandas as pd
from colorama import Fore
import glob
import sys
from timeit import default_timer as timer
from datetime import timedelta
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(".", '..'))

from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from database import Database
import seaborn as sb
import matplotlib.pyplot as plt






class Classifiers(object):
	"""docstring for MLClustering."""

	def __init__(self, alg="tdea", experiments=1):
		self.alg = alg
		self.experiments = experiments
		self.target_filename = '../targetDatasets/test/target_{}.gzip'.format(alg)
		self.current_exp = 1
		self.training = self.__loadTrainingDataset()

		# self.target = self.__loadTargetDataset()
		self.target = self.__loadAllTargetDataset()

	def __loadTrainingDataset(self):
		files = glob.glob("../trainingDatasets/*.gzip")

		if files:
			df = pd.DataFrame(columns=['algorithm', 'entropy', 'nonce', 'output'])
			for filename in files:
				df_training = pd.read_parquet(filename, columns=None)
				df = df.append(df_training)
			# df['output'] = df['output'].apply(lambda x: int.from_bytes(x,"big"))
			return df.sample(frac=1).reset_index(drop=True)
		else:
			print('{}ERROR: Please, run generateTrainingDatasets.py to generate the training datasets{}'.format(
				Fore.RED,Fore.RESET
			))


	def __loadTargetDataset(self):
		if os.path.isfile(self.target_filename):
			data = pd.read_parquet(self.target_filename, columns=None)
		else:
			data = Database().get_all_data_by_algorithm(self.alg)
			data.to_parquet(self.target_filename)
		return data

	def __loadAllTargetDataset(self):
		files = glob.glob("../targetDatasets/test/*.gzip")

		if files:
			df = pd.DataFrame(columns=['algorithm', 'entropy', 'nonce', 'output'])
			for filename in files:
				df_target = pd.read_parquet(filename, columns=None)
				df = df.append(df_target)
			# df['output'] = df['output'].apply(lambda x: int.from_bytes(x,"big"))
			return df.sample(frac=1).reset_index(drop=True)
		else:
			print('{}ERROR: Please, run generateTrainingDatasets.py to generate the training datasets{}'.format(
				Fore.RED,Fore.RESET
			))



	def knn(self):
		sb.pairplot(self.training, hue='algorithm', size=7, vars=["output"], kind='scatter')
		plt.show()
		X = self.training.drop(['algorithm','entropy','nonce'], axis=1)
		Y = self.training['algorithm']
		X_test = self.target.drop(['algorithm','entropy','nonce'], axis=1)
		Y_test = self.target['algorithm']

		knn = KNeighborsClassifier(n_neighbors=3)
		knn.fit(X, Y)
		y_pred = knn.predict(X_test)

		print("Accuracy:",metrics.accuracy_score(Y_test, y_pred))
		# print("Precision:",metrics.precision_score(Y_test, y_pred))
		# print("Recall:",metrics.recall_score(Y_test, y_pred))

		return metrics.precision_score(Y_test, y_pred)


	def rf(self):
		from sklearn.ensemble import RandomForestClassifier
		#print("DecisionTreeClassifier")

		X = self.training.drop(['algorithm','entropy','nonce'], axis=1)
		Y = self.training['algorithm']
		X_test = self.target.drop(['algorithm','entropy','nonce'], axis=1)
		Y_test = self.target['algorithm']

		 #Instantiate the classifier
		self.rfc = RandomForestClassifier()
		# Train classifier
		start = timer()
		self.rfc.fit(X, Y)
		end = timer()
		y_pred = self.rfc.predict(X_test)

		print("Accuracy:", metrics.accuracy_score(Y_test, y_pred))
		print("Timing:",timedelta(seconds=end-start))




	def bayes(self):
		from sklearn.naive_bayes import GaussianNB

		X = self.training.drop(['algorithm','entropy','nonce'], axis=1)
		Y = self.training['algorithm']
		X_test = self.target.drop(['algorithm','entropy','nonce'], axis=1)
		Y_test = self.target['algorithm']

		# Instantiate the classifier
		self.gnb = GaussianNB()
		# Train classifier
		start = timer()
		self.gnb.fit(X, Y)
		end = timer()

		y_pred = self.gnb.predict(X_test)

		print("Accuracy:", metrics.accuracy_score(Y_test, y_pred))
		print("Timing:",timedelta(seconds=end-start))



# alg_list = ['tdea',
# 	'aes128', 'aes192', 'aes256',
# 	'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
# 	'sha1hmac','sha224hmac', 'sha256hmac', 'sha384hmac','sha512hmac']
# # alg_list = ["tdea"]

# m = dict(zip(alg_list,range(len(alg_list))))
# lab = lambda x : m[x]

# from debug import Classifiers

trainingsize 	= 2000
targetsize		= [100,10000]

sv = Classifiers(alg_list, training_size=trainingsize, target_sizes=targetsize)


sv.bayes()
# sv.rf()
# svm_cluster.knn()
# print(svm_cluster)

# ba = sv.gnb
# rf = svm_cluster.rfc

# X_test = sv.target.drop(['algorithm','entropy','nonce'], axis=1)
# Y_test = sv.target['algorithm']

# y_ba = ba.predict(X_test)
# y_ba_p = ba.predict_proba(X_test)
# # y_rf = rf.predict(X_test)



# print()
