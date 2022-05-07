from datetime import datetime
from threading import Thread
from requests import get

from src.database import Postgresql
from src.utils import Log
from src.config import get_config
from src.database import Preprocess


class Fetch:
    # <| Public Function |>
    def __init__(self, db: Postgresql, delay: int) -> None:
        self.__preprocess = Preprocess()

        self.run_timed = 0
        self.db = db
        self.delay = delay

    def process_with_cryptorank_api(self, time):
        if time - self.run_timed > self.delay:
            self.run_timed = time
            t = Thread(target=self.__process_with_cryptorank_api)
            t.start()

    #  <| Private Function |>

    @Log('Fetch')
    def __process_with_cryptorank_api(self):
        # latest news timestamp
        cur = self.db.execute(f"select Max(date) from News")
        max_date = cur.fetchone()[0]
        # setup url
        url = get_config(['news_source', 'cryptorank'])
        url = f"{url}?limit={100}&lang=en&sourceIds=1,5,8,11,14,19,42"

        if max_date != None:
            max_date = int(datetime.timestamp(max_date)*1000) + 1
            url += f"&from={max_date}"

        # get data & preprocessing
        response = get(url).json()
        data = self.__preprocess.cryptorank_preprocess(
            response['data'])

        for news in data:
            self.__insert_news(news)

    def __insert_news(self, data):
        cur = self.db.conn.cursor()

        # INSERT NEWS |>
        cur.execute(f"""
            select id from News where title='{data['title']}' or url='{data['url']}';
        """)
        news_id = cur.fetchone()

        if news_id != None:
            return

        cur.execute(f"""
            insert into News (
                title,
                description,
                url,
                icon,
                source,
                major_url,
                minor_url,
                date
            )
            values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            returning id;
        """, (data['title'], data['description'], data['url'], data['icon'], data['source'], data['major_url'], data['minor_url'],datetime.fromtimestamp(data['date']/1000, tz=None) ))

        # Inserted News ID
        news_id = cur.fetchone()[0]

        # INSERT TAGS |>
        tags_id = []
        for tag in data['tags']:
            cur.execute(f"""
                select id from Tags where name='{tag['name']}' or key='{tag['key']}';
            """)
            tag_id = cur.fetchone()
            if tag_id == None:
                cur.execute(f"""
                    insert into Tags(name, key, symbol) values ('{tag['name']}', '{tag['key']}', '{tag['symbol']}')
                    returning id;
                """)
                tag_id = cur.fetchone()

            tags_id.append(tag_id[0])
        
        # INSERT NEWS_TAGS
        for tag_id in tags_id:
            cur.execute(f"""
                insert into News_Tags (news_id, tags_id) values ({news_id}, {tag_id});
            """)
        
        self.db.conn.commit()
        cur.close()
            