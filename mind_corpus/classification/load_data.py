import os
import json
import sys

from sklearn.model_selection import train_test_split


######################################################
# Functions
######################################################
def load_article(filepath):
    with open(filepath, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def load_from_path(subset_path, mode):
    subset = []
    child_dirs = next(os.walk(subset_path))[1]
    # Iterate over sources.
    for source in child_dirs:
        files = os.listdir('{}/{}'.format(subset_path, source))
        # Iterate over files.
        for filename in files:
            # Load json file.
            filepath = '{}/{}/{}'.format(subset_path, source, filename)
            data = load_article(filepath)
            if mode == 'headline':
                subset += [data['headline']]
            elif mode == 'body_text':
                subset += [data['body_text']]
            elif mode == 'headline_body_text':
                subset += [data['headline'] + ' ' + data['body_text']]
            else:
                print('Invalid mode.')
                sys.exit()
    return subset


def load_multiclass_corpus(paths, mode):
    texts, labels = [], []
    for c, path in enumerate(paths):
        subset_texts = load_from_path(path, mode)
        subset_labels = [c for i in subset_texts]
        texts += subset_texts
        labels += subset_labels
    # print(len(texts),len(labels))
    return texts, labels


def generate_splits(texts, labels):
    x_train, x, y_train, y = train_test_split(texts, labels, test_size=0.3, train_size=0.7, stratify=labels,
                                              random_state=42)
    x_val, x_test, y_val, y_test = train_test_split(x, y, test_size=0.5, train_size=0.5, stratify=y, random_state=42)
    return x_train, y_train, x_val, y_val, x_test, y_test
