import json
from pprint import pprint

from sklearn.metrics import classification_report, confusion_matrix


class ClassificationReport:
    def __init__(self, estimator, best_params, y_true, y_pred):
        self.estimator = estimator
        self.best_params = best_params
        self.y_true = y_true
        self.y_pred = y_pred

    def print(self):
        print(self.estimator)
        print("\nBest estimated parameters:")
        pprint(self.best_params)
        print("\nClassification report:")
        pprint(self.generate_classification_report())
        print("\nConfusion matrix:")
        pprint(self.generate_cm())

    def save(self, path):
        filepath = "{}/{}.json".format(path, self.estimator)
        report = {
            "best_params": self.best_params,
            "classification_report": self.generate_classification_report(),
            "confusion_matrix": self.generate_cm().tolist()
        }

        with open(filepath, 'w', encoding='utf-8') as outfile:
            json.dump(report, outfile, indent=4)

    def generate_classification_report(self):
        report_dict = classification_report(self.y_true, self.y_pred, output_dict=True)
        return report_dict

    def generate_cm(self):
        cm = confusion_matrix(self.y_true, self.y_pred)
        return cm
