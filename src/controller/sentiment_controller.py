from datetime import datetime, timedelta
from threading import Thread
from sqlalchemy.orm import Session


from src.config import get_config
from src.command import Sentiment
from src.util.logging import log_info

class SentimentController:
    def __init__(self, db: Session):
        self.execute_time = datetime.now().timestamp()
        self.delay = int(get_config(['interval_config', 'sentiment_delay']))
        self.sentiment = Sentiment(db)
    
    def luanch(self, time: float):
        if self.execute_time <= time:
            log_info("sentiment analyze...")

            self._increment_execute_time()
            worker_cryptorank = Thread(target=self.sentiment.analyze)
            worker_cryptorank.start()

    def _increment_execute_time(self):
        self.execute_time = (datetime.fromtimestamp(self.execute_time) + timedelta(minutes=self.delay)).timestamp()