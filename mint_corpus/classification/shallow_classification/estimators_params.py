from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

random_forest = {
    "estimator": RandomForestClassifier(random_state=42),
    "param_grid": {
        "criterion": ["gini", "entropy"],
        "max_depth": [None, 2, 4, 8, 16, 32],
        "min_samples_split": [2, 4, 8, 16, 32],
        "min_samples_leaf": [1, 2, 4, 8, 16, 32],
    }
}

svc = {
    "estimator": SVC(random_state=42),
    "param_grid": {
        "kernel": ["linear", "rbf", "poly", "sigmoid"],
        "C": [0.1, 1, 10, 100],
        # "gamma": [1, 0.1, 0.01, 0.001],
        # "gama": ["auto", "scale"],
        "probability": [True, False],
        "class_weight": ["balanced"]
    }
}

logistic_regression = {
    "estimator": LogisticRegression(random_state=42),
    "param_grid": {
        "penalty": ["l1", "l2"],
        "C": [0.1, 1, 10, 100],
        "solver": ["saga", "lbfgs"],
        "multi_class": ["auto"]
    }
}
