from threading import Thread
from src.database.postgresql import Postgresql
from src.utils.logger import Log
from .scraper import Scraper
from src.config import get_config

SCRAPING_LIMIT = int(get_config(['miner_config', 'scraping_limit']))

class Miner:
    # <| Public Function |>
    def __init__(self, db: Postgresql, delay=3):
        self.run_timed = 0  # executed time
        self.delay = delay  # execution delay of @mining
        self.scraper = Scraper()  # define Scraper
        self.db = db  # define database

        # on build

    # interval execute core process process function
    def mining_cryptorank(self, time):
        if time - self.run_timed > self.delay:
            print("<------------- MINING ------------->")
            self.run_timed = time
            t = Thread(target=self.__process_cryptorank)
            t.start()
    
    # <| Private Function |>
    # core process function
    def __process_cryptorank(self):
        # All not scraping news
        cur = self.db.execute(f"select id, source, url from News where text is null order by date desc limit {SCRAPING_LIMIT};")
        result = cur.fetchall()
        data = []
        for item in result:
            data.append({
                'id':item[0],
                'source':str(item[1]).strip(),
                'url':item[2]
            }) 
        
        # All config
        cur.execute(f"select source, xpath from source_configs;")
        result = cur.fetchall()
        config_scrap = {}
        for item in result:
            config_scrap[str(item[0]).strip()] = str(item[1]).strip()
        print(config_scrap)

        # Scraping
        for news in data:
            text = self.scraper.scraping(news['url'], config_scrap[news['source']])
            text = text.replace("'", "''")
            cur.execute(f"""
                update News set text='{text}' where id={news['id']};
            """)

        self.db.conn.commit()
        cur.close()

        self._delete_empty()

    Log('Miner')
    def _delete_empty(self):
        self.db.execute_commit(f"delete from news_tags using news where news.text='';")
        self.db.execute_commit(f"delete from news where text='';")
        