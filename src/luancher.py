from datetime import datetime
from time import sleep
from src.fetch.fetch import Fetch
from src.scraping import Scraper, scraper
from src.scraping import Miner
from src.database import Postgresql
from src.config import get_config


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
        # @table: News
        self.db.execute_commit(f"""
            CREATE TABLE IF NOT EXISTS News(
                id serial,
                title char(256) not null unique,
                description char(1000) not null,
                url char(500) not null unique,
                tags char(256),
                icon char(500),
                source char(64) not null,
                major_url char(100) not null,
                minor_url char(64),
                text text,
                polarity decimal,
                sentiment varchar(32),
                date timestamp,

                primary key (id)
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

                primary key (id)
            )
        """)

        # <|- Database
        self.miner = Miner(db=self.db, delay=1)
        self.fetch = Fetch(db=self.db, delay=5)

    # provider of interval execute methods.
    def update(self):
        while True:
            now = datetime.now()

            self.fetch.process_with_cryptorank_api(now.minute)

            # delay loop 1 second
            sleep(1)
