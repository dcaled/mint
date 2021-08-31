import os
import json
from pprint import pprint


class CrawledArticle:
    def __init__(self, filename, category, source, url, publish_date, headline, body_text, authors=None,
                 description=None, tags=None, top_image=None, movies=None):
        self.filename = filename
        self.category = category
        self.source = source
        self.url = url
        self.publish_date = publish_date
        self.headline = headline
        self.body_text = body_text
        self.authors = authors
        self.description = description
        self.tags = tags
        self.top_image = top_image
        self.movies = movies

    def print(self):
        pprint(self.__dict__)

    def save_article(self, path, filename):
        filepath = '{}{}/{}.json'.format(path, self.source, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(self.__dict__, file, indent=4, sort_keys=True)

