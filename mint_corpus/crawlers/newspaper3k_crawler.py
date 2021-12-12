import json
import logging
from tqdm import tqdm

from newspaper import Article, Config, ArticleException
import mint_corpus.constants as const
from crawled_article import CrawledArticle

log_path = '{}/newspaper3k.log'.format(const.fp_logs)
logging.basicConfig(filename=log_path, level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


def save_article(path, metadata, article):
    crawled_article = CrawledArticle(
        filename=metadata["filename"],
        category=metadata["category"],
        source=metadata["source"],
        url=metadata["url"],
        publish_date=metadata["publish_date"],
        headline=metadata["headline"],
        body_text=article.text.strip(),
        authors=metadata["authors"],
        description=metadata["description"],
        tags=metadata["tags"],
        top_image=metadata["top_image"],
        movies=metadata["movies"]
    )
    # crawled_article.print()
    crawled_article.save_article(path)


def crawl_url(path, metadata):
    try:
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
        n3k_config = Config()
        n3k_config.browser_user_agent = user_agent

        article = Article(metadata["url"], config=n3k_config)
        article.download()
        article.parse()
        if not article.text.strip():
            err = "\nFailed to download {}. No body text found.".format(metadata["url"])
            print(err)
            logging.exception('Exception: {}'.format(err))
            return False
        else:
            save_article(path, metadata, article)
            return True
    except ArticleException as err:
        print("\nFailed to download {}. URL not found.".format(metadata["url"]))
        logging.exception('Exception: {}'.format(err))
        return False
    except Exception as err:
        print(err)
        logging.exception('Exception: {}'.format(err))
        return False


def main():
    with open(const.fp_mint_metadata, encoding='utf-8') as json_file:
        mint_metadata = json.load(json_file)

    print("Downloading subsets - Starting...")
    print()
    crawler_status = {"success": 0, "fail": 0}

    for entry in tqdm(mint_metadata[19000:]):
        if entry["source"] in ["resistir"]:
            current_status = crawl_url(const.fp_mint_corpus, entry)
            if current_status:
                crawler_status["success"] += 1
            else:
                crawler_status["fail"] += 1
    print("Downloading subsets - Complete (Retrieved {} news articles. Failed {} news articles).".format(
        crawler_status["success"], crawler_status["fail"]))
    print()


if __name__ == '__main__':
    main()
