# MIND Corpus
Danielle Caled and Paula Carvalho and Mário J. Silva. 2021. MIND - Mainstream and Independent News Documents Corpus

Paper: https://arxiv.org/abs/2108.06249

MIND (Mainstream and Independent News Documents) is a corpus composed of 20,278 articles from 33 Portuguese mainstream and independent media, aiming at covering different styles, subjects, and communication purposes.
The collection period ranges from June 1st, 2020 to March 31st, 2021, representing a full year sample of online content published in Portuguese media.
The articles are organized into five categories, classified as *facts*, *opinions*, *entertainment*, *satires*, and *conspiracy theories*.


We make MIND corpus metadata available in this repository. 
To allow the access to news articles' headline and body text, we implement a series of scrappers, customized according to the source of the article.


## Instructions

### Download metadata

Metadata are available [here](https://github.com/dcaled/mind/blob/master/mind_corpus/corpus/mind_metadata.json).

### Download text 

For convenience, we have provided a script which will download the news articles for you. Please follow the instructions if you would like to use the attached script.

Fork or clone this repository and install required python libraries:

```
$ git clone https://github.com/dcaled/mind.git
$ cd mind
$ conda env create --file environment.yml
```

Download the news articles with the provided scripts:

```
$ cd mind_corpus/crawlers
$ python donwload_mind.py
```

Access the corpus data in ```mind/mind_corpus/corpus```.

## Disclaimer
MIND's news articles are downloaded directly from their source URLs through the scrappers provided in this repository. Since source pages are dynamic, their content may not be available or may be updated at the time of download.


## Citation
```
@misc{caled2021mind,
      title={MIND - Mainstream and Independent News Documents Corpus}, 
      author={Danielle Caled and Paula Carvalho and Mário J. Silva},
      year={2021},
      eprint={2108.06249},
      archivePrefix={arXiv},
}
```
