import pandas as pd
import numpy as np
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from schemes.categorical_neighbourhood.categorical_neighbourhood import CategoricalNeighbourhood
from sklearn.linear_model import LogisticRegression

from utils import *
from time import time

gamma = 1

# 0) import data
breast_cancer, primary_key = import_dataset("breast_cancer_full")
breast_cancer = breast_cancer.drop('Id', axis=1)

# 1) calculate benchmark hyperparameters that will be used in all experiments with Decision Tree

# 1.1) get dummies from the categorical data
c = len(breast_cancer.columns)
target = breast_cancer.values[:, (c-1)]
breast_cancer = breast_cancer.drop("recurrence", axis=1)
breast_cancer = pd.get_dummies(breast_cancer)
data = breast_cancer.values

# 1.2) define the model and possible hyperparameters
random_state = 25 # increase every run
solver_range = ["liblinear", "newton-cg", "lbfgs", "saga"]
C_range = range(10, 101, 10)

n_exp = 5
start = time()
results = []
for n in range(n_exp):
    random_state = 2*n+1
    # 2) stratify data into main data and test holdout
    X_data, X_holdout, y_data, y_holdout = train_test_split(data, target, test_size=0.25, stratify=target, random_state=random_state)

    # 3) train a model on original data
    # 3.1) find the best hyperparameters
    model = LogisticRegression(random_state=random_state)
    param_dist = dict(C=C_range, solver=solver_range)
    rand_search = RandomizedSearchCV(model, param_dist, cv=10, n_iter=10, scoring="accuracy", random_state=random_state)
    rand_search.fit(data, target)
    best_params = rand_search.best_params_
    # 3.2) train
    model = LogisticRegression(C=best_params['C'], solver=best_params['solver'], random_state=0)
    model.fit(X_data, y_data)

    # 4) evaluate the original on holdout
    result_original = model.score(X_holdout, y_holdout)

    # 5) fingerprint the data
    # 5.1) define a scheme
    scheme = CategoricalNeighbourhood(gamma=gamma, xi=2, fingerprint_bit_length=8)
    # 5.2) fingerprint the data
    secret_key = 2322  # increase every run
    fp_dataset = scheme.insertion(dataset_name="breast_cancer", buyer_id=1, secret_key=secret_key)
    fp_dataset = fp_dataset.drop("Id", axis=1)
    print(type(fp_dataset))

    # 6) train the model with fingerprinted data

    # 6.1) preprocess the fingerprinted data (get dummies)
    fp_dataset = pd.get_dummies(fp_dataset)
    # check for missing columns and fill with zeros
    if not fp_dataset.columns.equals(breast_cancer.columns):
        print("DETECTED")
        difference = breast_cancer.columns.difference(fp_dataset.columns)
        print(difference)
        for diff in difference:
            fp_dataset[diff] = np.zeros((len(fp_dataset),), dtype=np.int)
    fp_dataset = fp_dataset[breast_cancer.columns.tolist()]
    data_fp = fp_dataset.values

    # 6.2) filter-out the holdout
    X_data_fp, X_holdout_fp, y_data_fp, y_holdout_fp = train_test_split(data_fp, target, test_size=0.25, stratify=target, random_state=random_state)

    # 6.3) train the model
    model2 = LogisticRegression(C=best_params['C'], solver=best_params['solver'], random_state=0)
    model2.fit(X_data_fp, y_data)

    # 7) evaluate on the holdout
    print(len(X_data_fp[0]))
    result_fp = model2.score(X_holdout, y_holdout)

    results.append(result_fp-result_original)
    print("Original: " + str(result_original) + "; Fingerprinted: " + str(result_fp))

print("Time: " + str(int(time()-start)) + " seconds.")
print("Results: " + str(results))
print("Average: " + str(np.mean(results)))
print("Breast Cancer; gamma=" + str(gamma))