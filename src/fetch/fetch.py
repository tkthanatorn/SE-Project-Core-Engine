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
        # load url
        url = get_config(['news_source', 'cryptorank'])
        url = f"{url}?limit={100}&lang=en&sourceIds=1,5,8,11,14,19,42"

        # get data & preprocessing
        response = get(url).json()
        data = self.__preprocess.cryptorank_preprocess(
            response['data'])

        # generate query
        query_value = ''
        for i in range(len(data['title'])):
            query_value += f",('{data['title'][i]}', '{data['description'][i]}', '{data['url'][i]}', '{data['tags'][i]}', '{data['icon'][i]}', '{data['source'][i]}', {data['date'][i]}, '{data['major_url'][i]}', '{data['minor_url'][i]}')"
        query = f"insert into news (title, description, url, tags, icon, source, date, major_url, minor_url) values {query_value[1:]};"
        self.db.execute_commit(query)
