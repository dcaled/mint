from tqdm import tqdm
import spacy
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

sp = spacy.load('pt_core_news_sm')


def tokenize_sentences(document):
    sent_tokens = sent_tokenize(document)
    sentences = []
    for token in sent_tokens:
        sentences += token.split('\n')
    return sentences


def tokenize_words(sentences):
    tokens = []
    for i in range(len(sentences)):
        for word in sp(sentences[i]):
            # Ignore punctuation.
            if word.pos_ != 'PUNCT':
                tokens += [word.text.lower()]
    return tokens


def vectorize_subset(subset):
    vectorized_subset = []
    for doc in tqdm(subset):
        sentences = tokenize_sentences(doc)
        words = tokenize_words(sentences)
        vectorized_subset += [' '.join(words)]
    return vectorized_subset


def vectorize_corpus(corpus_train, corpus_val, corpus_test, max_features=None):
    """First performs sentence tokenization, word tokenization, and then vectorizes the documents."""
    print("------------------------------\n")
    print('Vectorizing {} documents.'.format(len(corpus_train + corpus_val + corpus_test)))
    print("------------------------------\n")

    print('Vectorizing training subset:')
    vectorized_corpus_train = vectorize_subset(corpus_train)
    print('\nVectorizing validation subset:')
    vectorized_corpus_val = vectorize_subset(corpus_val)
    print('\nVectorizing testing subset:')
    vectorized_corpus_test = vectorize_subset(corpus_test)

    vectorizer = CountVectorizer(lowercase=False, max_features=max_features)
    x_train = vectorizer.fit_transform(vectorized_corpus_train)
    x_val = vectorizer.transform(vectorized_corpus_val)
    x_test = vectorizer.transform(vectorized_corpus_test)
    return x_train, x_val, x_test
