from datetime import datetime
from sqlalchemy.orm import Session
from time import sleep
from src.util.logging import log_info

from src.database import SourceConfigDatabase
from src.config import engine
from src.config import SessionLocal
from src.model import SourceConfigs
from src import model
from src.controller import FetchController, MinerController, SentimentController


def initialize(db: Session):
    sc_db = SourceConfigDatabase(db)
    try:
        sc1 = SourceConfigs(source="Cointelegraph", major_url="cointelegraph.com", xpath='//*[@class="post-content"]')
        sc_db.save(sc1) 
        sc2 = SourceConfigs(source="AMBCrypto", major_url="ambcrypto.com",xpath='//*[@id="mvp-content-main"]')
        sc_db.save(sc2) 
        sc3 = SourceConfigs(source="U.Today", major_url="u.today", xpath='//*[@class="article__content"]')
        sc_db.save(sc3) 
        sc4 = SourceConfigs(source="Bitcoin News", major_url="news.bitcoin.com", xpath='//*[@class="article__body"]')
        sc_db.save(sc4) 
        sc5 = SourceConfigs(source="Finance Magnates", major_url="www.financemagnates.com", xpath='//*[@class="article-body"]')
        sc_db.save(sc5) 
        sc6 = SourceConfigs(source="Coingape", major_url="coingape.com", xpath='//*[@class="main c-content"]')
        sc_db.save(sc6) 
        sc7 = SourceConfigs(source="The Daily Hodl", major_url="dailyhodl.com", xpath='//*[@class="content-inner "]')
        sc_db.save(sc7)
    except Exception as e:
        pass

    

def luancher():
    model.Base.metadata.create_all(engine)
    db = SessionLocal()
    fetch_controller = FetchController(db)
    miner_controller = MinerController(db)
    sentiment_controller = SentimentController(db)
    initialize(db)

    while True:
        now = datetime.now()
        log_info("-"*20)
        fetch_controller.luanch(now.timestamp())
        miner_controller.luanch(now.timestamp())
        sentiment_controller.luanch(now.timestamp())
        sleep(1)
