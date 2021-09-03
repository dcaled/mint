from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

random_forest = {
    "estimator": RandomForestClassifier(random_state=42),
    "param_grid": {
        'max_depth': [3, 5, 10],
        'min_samples_split': [2, 5, 10]
    }
}

svc = {
    "estimator": SVC(random_state=42),
    "param_grid": {
        'C': [0.1, 1, 10, 100],
        'gamma': [1, 0.1, 0.01, 0.001],
        'kernel': ['rbf', 'poly', 'sigmoid']
    }
}

logistic_regression = {
    "estimator": LogisticRegression(random_state=42),
    "param_grid": {
        'C': [0.1, 0.5, 1, 5, 10, 50, 100]
    }
}