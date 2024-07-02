from pymongo import MongoClient, errors


class TorScrapingDatabase:

    def __init__(self):
        # MongoDB configuration
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['tor_crawler']
        self.urls_collection = self.db['urls']

    def save_url_to_db(self, url: str, crawled: bool, raw_html: str = None, links: list = None):
        try:
            self.urls_collection.update_one(
                {'url': url},
                {'$set': {
                    'url': url,
                    'crawled': crawled,
                    'raw_html': raw_html,
                    'links': links}
                },
                upsert=True)
        except errors.PyMongoError as e:
            print(f"Error saving URL to database: {e}")

    def get_all_urls(self):
        try:
            return self.urls_collection.find()
        except errors.PyMongoError as e:
            print(f"Error fetching URLs from database: {e}")
            return

    def get_next_url(self):
        try:
            next_url = self.urls_collection.find_one({'crawled': False})
            if next_url:
                return next_url['url']
            else:
                return None
        except errors.PyMongoError as e:
            print(f"Error fetching next URL from database: {e}")
            return None
