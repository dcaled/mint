import os
import pickle
import sys

from scipy import sparse
from sklearn.model_selection import GridSearchCV, PredefinedSplit

import mind_corpus.constants as const
import mind_corpus.classification.load_data as load
from mind_corpus.classification.shallow_classification.classification_report import ClassificationReport
from estimators_params import random_forest, svc, logistic_regression
import preprocess


def load_or_create_preprocessed_corpus(paths_to_subsets, path_to_preprocessed_corpus, mode):
    """Load or create BOW representations for the corpus."""
    path_to_texts = "{}/{}_texts.pkl".format(path_to_preprocessed_corpus, mode)
    path_to_labels = "{}/{}_labels.pkl".format(path_to_preprocessed_corpus, mode)
    # Check if files are already created.
    if os.path.isfile(path_to_texts) and os.path.isfile(path_to_labels):
        with open(path_to_texts, 'rb') as f:
            x = pickle.load(f)
        print('Texts loaded from file.')
        with open(path_to_labels, 'rb') as f:
            y = pickle.load(f)
        print('Labels loaded from file.')
    # Create preprocessed corpus files.
    else:
        # Loading corpus from disk.
        texts, labels = load.load_multiclass_corpus(paths_to_subsets, mode)
        # Generating corpus splits.
        x_train, y_train, x_val, y_val, x_test, y_test = load.generate_splits(texts, labels)
        # Vectorizing the corpus.
        x_train, x_val, x_test = preprocess.vectorize_corpus(x_train, x_val, x_test, max_features=100)

        x = {"x_train": x_train, "x_val": x_val, "x_test": x_test}
        y = {"y_train": y_train, "y_val": y_val, "y_test": y_test}

        with open(path_to_texts, 'wb') as f:
            pickle.dump(x, f, protocol=4)
        print("Corpus' texts preprocessed and stored in disk.")
        with open(path_to_labels, 'wb') as f:
            pickle.dump(y, f, protocol=4)
        print("Corpus' labels preprocessed and stored in disk.")
    return x, y


def run_grid_search(model, params, x_train, y_train, pds):
    grid = GridSearchCV(model, params, cv=pds, n_jobs=-1, scoring='f1_macro', verbose=0, refit=True)
    grid.fit(x_train, y_train)
    return grid, grid.best_params_, grid.best_score_


def main():
    path_to_corpus = "../../corpus"
    path_to_preprocessed_corpus = "../../corpus"
    path_to_results = "results"

    # Creating logs directory.
    if not os.path.exists(path_to_results):
        os.makedirs(path_to_results)

    subsets = ['fact', 'opinion', 'entertainment', 'satire', 'conspiracy']
    paths_to_subsets = ["{}/{}".format(path_to_corpus, subset) for subset in subsets]

    MODES = ["headline"]
    for mode in MODES:
        # Loading corpus:
        x, y = load_or_create_preprocessed_corpus(paths_to_subsets, path_to_preprocessed_corpus, mode)

        # Create a list where train data indices are -1 and validation data indices are 0
        split_index = [-1 for i in x["x_train"]] + [0 for i in x["x_val"]]
        x_train_val = sparse.vstack((x["x_train"], x["x_val"]))
        y_train_val = y["y_train"] + y["y_val"]
        pds = PredefinedSplit(test_fold=split_index)

        # Run RandomForestClassifier.
        grid, best_params, best_score = run_grid_search(random_forest["estimator"], random_forest["param_grid"],
                                                        x_train_val, y_train_val, pds)
        report = ClassificationReport("random_forest", best_params, y["y_test"], grid.predict(x["x_test"]))
        report.print()
        # report.save(path_to_results)

        # Run SVC.
        grid, best_params, best_score = run_grid_search(svc["estimator"], svc["param_grid"],
                                                        x_train_val, y_train_val, pds)
        report = ClassificationReport("svc", best_params, y["y_test"], grid.predict(x["x_test"]))
        report.print()

        # Run LogisticRegression.
        grid, best_params, best_score = run_grid_search(logistic_regression["estimator"],
                                                        logistic_regression["param_grid"], x_train_val, y_train_val,
                                                        pds)
        report = ClassificationReport("logistic_regression", best_params, y["y_test"], grid.predict(x["x_test"]))
        report.print()


if __name__ == '__main__':
    main()
