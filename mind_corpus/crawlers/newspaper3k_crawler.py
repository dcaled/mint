import json
import logging
import sys

from newspaper import Article, Config
from crawled_article import CrawledArticle


def save_article(path, metadata, article):
    crawled_article = CrawledArticle(
        filename=metadata["filename"],
        category=metadata["category"],
        source=metadata["source"],
        url=metadata["url"],
        publish_date=metadata["publish_date"],
        headline=article.title,
        body_text=article.text,
        authors=metadata["authors"],
        description=metadata["description"],
        tags=metadata["tags"],
        top_image=metadata["top_image"],
        movies=metadata["movies"]
    )
    crawled_article.print()
    crawled_article.save_article(path)


def crawl_url(path, metadata):
    try:
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
        n3k_config = Config()
        n3k_config.browser_user_agent = user_agent

        article = Article(metadata["url"], config=n3k_config)
        article.download()
        article.parse()
        if not article.title:
            print("title")
            sys.exit()
            pass
        elif not article.text:
            print("text")
            sys.exit()
            # TODO
            pass
        save_article(path, metadata, article)
    except Exception as err:
        print(err)
        logging.exception('Exception: {}'.format(err))


def main():
    metadata_filepath = "../corpus/mind_metadata.json"
    corpus_filepath = "../corpus"

    with open(metadata_filepath, encoding='utf-8') as json_file:
        mind_metadata = json.load(json_file)

    for entry in mind_metadata[0:6000]:
        if entry["category"] == "fact":
            if entry["source"] in ["cmjornal", "dn", "publico", "sicnoticias"]:
                crawl_url(corpus_filepath, entry)
            elif entry["source"] == ["expresso", "jn", "jornaldenegocios", "tsf"]:
                # TODO: Fix body text start. Requires preprocess.
                pass
            # elif entry["source"] == "new_source":
            #     crawl_url(corpus_filepath, entry)
            elif entry["source"] == ["lusa"]:
                # TODO: Upload these content directly onto repo.
                pass
        else:
            # TODO: to be implemented...
            pass


if __name__ == '__main__':
    main()
