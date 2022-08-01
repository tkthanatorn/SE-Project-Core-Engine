from sqlalchemy.orm import Session
from src.database import NewsDatabase, SourceConfigDatabase
from .util.scraper import Scraper
from src.config import get_config

_SCRAPING_LIMIT = int(get_config(['miner_config', 'scraping_limit']))


class Miner:
    def __init__(self, db: Session):
        self.scraper = Scraper()
        self.news_db = NewsDatabase(db)
        self.sc_db = SourceConfigDatabase(db)
    
    def mining_cryptorank(self):
        data = self.news_db.get_null_text(_SCRAPING_LIMIT)
        news = list()
        for item in data:
            news.append({
                'id': item.id,
                'source': item.source,
                'url': item.url
            })

        data = self.sc_db.all()
        scs = dict()
        for item in data:
            scs[item.source] = item.xpath
        
        for i in range(len(news)):
            text = self.scraper.scraping(news[i]['url'], scs[news[i]['source']])
            if len(text) > 0:
                self.news_db.update(news[i]['id'], {"text": text})
            else:
                self.news_db.delete(news[i]['id'])


    
    