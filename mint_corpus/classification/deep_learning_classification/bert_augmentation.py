import json
import os

from tqdm import tqdm
import mint_corpus.classification.load_data as load

import nlpaug.augmenter.word as naw


def main():
    path_to_corpus = "../../corpus"
    path_to_augmented_corpus = "{}/augmentation".format(path_to_corpus)

    subsets = ["fact", "opinion", "entertainment", "satire", "conspiracy"]
    paths_to_subsets = ["{}/{}".format(path_to_corpus, subset) for subset in subsets]

    PRE_TRAINED_MODEL_NAME = 'bert-base-multilingual-cased'
    class_names = ['factual', 'opinion', 'entertainment', 'satire', 'conspiracy']

    modes = ["headline", "body_text", "headline_body_text"]

    # Augment by BERT
    aug = naw.ContextualWordEmbsAug(model_path=PRE_TRAINED_MODEL_NAME, aug_p=0.1)

    for mode in modes:
        # Loading corpus from disk.
        texts, labels = load.load_multiclass_corpus(paths_to_subsets, mode)
        # Generating corpus splits.
        x_train, y_train, x_val, y_val, x_test, y_test = load.generate_splits(texts, labels)

        # Augmenting corpus for classes satire and conspiracy.
        aug_data = {'satire': dict(), 'conspiracy': dict()}
        for l, label in tqdm(enumerate(y_train[:])):
            if label in [3, 4]:
                category = class_names[label]
                text = x_train[l]
                aug_data[category][text] = dict()
                # Create 5 new instances from a given input.
                for j in range(5):
                    aug_data[category][text][j] = aug.augment(text)

        # Create augmented folder if it does not exist.
        if not os.path.exists(path_to_augmented_corpus):
            os.makedirs(path_to_augmented_corpus)

        # Save augmented data.
        filename = "{}/aug_data_{}_p0.1.json".format(path_to_augmented_corpus, mode)
        with open(filename, "w", encoding='utf-8') as jsonfile:
            json.dump(aug_data, jsonfile, ensure_ascii=False)


if __name__ == '__main__':
    main()
