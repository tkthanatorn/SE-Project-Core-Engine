from datetime import datetime
from requests import get
from sqlalchemy.orm import Session
from src.model import News, Tags

from src.config import get_config 
from src.command.util.preprocessing import cryptorank_preprocess
from src.util.logging import log_error, log_info

_INCREMENT_TIMESTAMP = get_config(["news_config", "increment_timestamp"])
_START_TIMESTAMP = get_config(["news_config", "start_timestamp"])


class Fetch:
    def __init__(self, db: Session):
        from src.database import NewsDatabase, TagsDatabase
        self.news_db = NewsDatabase(db)
        self.tags_db = TagsDatabase(db)
    
    def fetch_cryptorank(self):
        max_date = self.news_db.latest_news_date()

        url = get_config(["news_source", 'cryptorank'])
        url = f"{url}?limit={100}&lang=en&sourceIds=1,5,8,11,14,19,42"

        if max_date != None:
            max_date = int(datetime.timestamp(max_date) * 1000) + 1
            url += f"&from={max_date}&to={max_date + _INCREMENT_TIMESTAMP}"
            log_info(f"fetching cryptorank from {max_date} to {max_date + _INCREMENT_TIMESTAMP}")
        else:
            url += f"&form={_START_TIMESTAMP}&to={_START_TIMESTAMP + _INCREMENT_TIMESTAMP}"
            log_info(f"fetching cryptorank from {_START_TIMESTAMP} to {_START_TIMESTAMP + _INCREMENT_TIMESTAMP}")
        
        
        response = get(url).json()
        data = cryptorank_preprocess(response['data'])
        log_info(f"news incoming {len(data)} news.")
        for item in data:
            try:
                self.insert_cryptorank(item)
            except Exception as e:
                log_error(e)
    
    def insert_cryptorank(self, data: dict):
        news = News(
            title=data['title'],
            description=data['description'],
            url=data['url'],
            icon=data['icon'],
            source=data['source'],
            major_url=data['major_url'],
            minor_url=data['minor_url'],
            text=None,
            polarity=None,
            sentiment=None,
            date=datetime.fromtimestamp(data['date']/1000, tz=None)
        )

        for tag in data['tags']:
            tags = self.tags_db.findByName(tag['name'])
            if tags == None:
                tags = Tags(
                    name=tag['name'],
                    key=tag['key'],
                    symbol=tag['symbol']
                )
                self.tags_db.save(tags)
            news.tags.append(tags)
        
        self.news_db.save(news)
        

        