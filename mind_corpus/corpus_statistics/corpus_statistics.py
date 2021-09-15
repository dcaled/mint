import os
import json
import statistics
from tqdm import tqdm

from mind_corpus import constants
from preprocessed_article import PreprocessedArticle
from sentiment_metric import SentimentMetric


def load_article(filepath):
    with open(filepath, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def load_from_path(subset_path):
    subset = []
    child_dirs = next(os.walk(subset_path))[1]
    # Iterate over sources.
    for source in tqdm(child_dirs):
        files = os.listdir('{}/{}'.format(subset_path, source))
        # Iterate over files.
        for filename in files:
            # Load json file.
            filepath = '{}/{}/{}'.format(subset_path, source, filename)
            data = load_article(filepath)
            article = PreprocessedArticle(headline=data["headline"], body=data['body_text'])
            subset += [article]
    return subset


def compute_sentiment_metrics(subset):
    sentiment_metric = SentimentMetric()
    sentiment_metric.load_lexicon(constants.fp_lex_sent)

    metrics_names = ['sentiment_ratio', 'positive_ratio', 'negative_ratio', 'positive_contrast', 'negative_contrast']
    sentiment_metrics = {
        'headline': {k: [] for k in metrics_names},
        'body_text': {k: [] for k in metrics_names},
    }

    for article in tqdm(subset):
        sentiment_headline = sentiment_metric.compute_metric(text_as_list=article.headline_as_list)
        sentiment_body_text = sentiment_metric.compute_metric(text_as_list=article.body_as_list)
        for metric in metrics_names:
            sentiment_metrics['headline'][metric] += [sentiment_headline[metric]]
            sentiment_metrics['body_text'][metric] += [sentiment_body_text[metric]]
    return sentiment_metrics


def compute_average(metrics):
    for key, val in metrics.items():
        for metric_name, metric_values in val.items():
            print(key, metric_name, statistics.mean(metric_values), statistics.stdev(metric_values))


def main():
    path_to_corpus = "../corpus"
    subsets = ['fact', 'opinion', 'entertainment', 'satire', 'conspiracy']

    for subset in subsets:
        print("Loading {}...".format(subset))
        subset_texts = load_from_path("{}/{}".format(path_to_corpus, subset))

        print("Computing sentiment metrics for {}...".format(subset))
        sentiment_metrics = compute_sentiment_metrics(subset_texts)
        compute_average(sentiment_metrics)


if __name__ == '__main__':
    main()
