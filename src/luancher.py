from datetime import datetime
from time import sleep
from src.fetch.fetch import Fetch
from src.scraping import Miner
from src.database import Postgresql
from src.config import get_config

FETCH_DELAY = int(get_config(['interval_config', 'fetch_delay']))
MINER_DELAY = int(get_config(['interval_config', 'miner_delay']))


class Launcher:
    def __init__(self) -> None:
        # ?Database -|>
        # TODO: initialize database
        db_config = get_config(['database', 'dev'])
        self.db = Postgresql(
            host=db_config['host'],
            port=db_config['port'],
            username=db_config['username'],
            password=db_config['password'],
            dbname=db_config['dbname']
        )

        # TODO: setup tables
        # !DROP
        self.db.execute_commit(f"""
            DROP TABLE Source_Configs;
        """)

        # @table: News
        self.db.execute_commit(f"""
            CREATE TABLE IF NOT EXISTS News(
                id serial,
                title text not null unique,
                description text,
                url text not null unique,
                icon char(500),
                source char(64) not null,
                major_url char(100) not null,
                minor_url text,
                text text,
                polarity decimal,
                sentiment varchar(32),
                date timestamp,

                PRIMARY KEY (id)
            );
        """)

        # @table: sourceConfig
        self.db.execute_commit(f"""
            CREATE TABLE IF NOT EXISTS Source_Configs(
                id serial not null,
                source char(256) not null,
                major_url char(100) not null,
                minor_url char(64),
                xpath char(256),

                PRIMARY KEY (id)
            )
        """)

        # @table: Tags
        self.db.execute_commit(f"""
            CREATE TABLE IF NOT EXISTS Tags(
                id serial not null,
                name varchar(64) unique,
                key varchar(64) unique,
                symbol varchar(32),

                PRIMARY KEY (id)
            )
        """)

        # @table: News_Tags
        self.db.execute_commit(f"""
            CREATE TABLE IF NOT EXISTS News_Tags(
                id serial not null,
                news_id serial not null,
                tags_id serial not null,

                PRIMARY KEY (id),
                CONSTRAINT fk_news FOREIGN KEY(news_id) REFERENCES News(id), 
                CONSTRAINT fk_tags FOREIGN KEY(tags_id) REFERENCES Tags(id) 
            )
        """)

        # insert config
        self._insert_config()
        # <|- Database
        self.fetch = Fetch(db=self.db, delay=FETCH_DELAY)
        self.miner = Miner(db=self.db, delay=MINER_DELAY)

    # provider of interval execute methods.
    def update(self):
        while True:
            now = datetime.now()
            if now.second == 0:
                print(
                    f"time: {now.date()} {now.hour}:{now.minute}:{now.second} ------------------------------------------------------------------")

            self.fetch.process_with_cryptorank_api(now.minute)
            self.miner.mining_cryptorank(now.minute)
            # delay loop 1 second
            sleep(1)

    # insert config
    def _insert_config(self):
        self.db.execute_commit(f"""
        INSERT INTO Source_Configs(source, major_url, xpath) VALUES
        ('Cointelegraph', 'cointelegraph.com', '//*[@class="post-content"]'),
        ('AMBCrypto', 'ambcrypto.com', '//*[@id="mvp-content-main"]'),
        ('U.Today', 'u.today', '//*[@class="article__content"]'),
        ('Bitcoin News', 'news.bitcoin.com', '//*[@class="article__body"]'),
        ('Finance Magnates', 'www.financemagnates.com', '//*[@class="article-body"]'),
        ('Coingape', 'coingape.com', '//*[@class="main c-content"]'),
        ('The Daily Hodl', 'dailyhodl.com', '//*[@class="content-inner "]');
        """)
