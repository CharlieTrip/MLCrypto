# Modelling Cryptographic Distinguishers Using Machine Learning - Code 

---

*Published Paper:* [Journal of Cryptographic Engineering (Vol. 12 2022)](https://doi.org/10.1007/s13389-021-00262-x)

*Project Page:* [link](https://charlietrip.neocities.org/projects/old-mlcrypto)

---

*Old code directly from the archive. Published with minor clean-up!*

I'm reposting the code since I no longer have access to the
[original repo](https://bitbucket.org/CharlieTrip/mlcryptocode/src/master/).

---

### Content of the Repo

* `algorithms`: all the NIST DRBGs
* `experiments_cvs/plots.R`: code for plotting the obtained CSV (as in the paper)
* `ml`: the machine learning framework used
* `targetDatasets` and `trainingDatasets`: temporary folder for target and training dataset
* `main.py`: main code to execute the experiment and contains the experiment parameters

---

### Quick Usage

* Modify the experimental parameters in `main.py`
* Run `main.py` 
