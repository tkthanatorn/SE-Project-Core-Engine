from threading import Thread

from src.database.postgresql import Postgresql

from .scraper import Scraper


class Miner:
    # <| Public Function |>
    def __init__(self, db: Postgresql, delay=3):
        self.run_timed = 0  # executed time
        self.delay = delay  # execution delay of @mining
        self.scraper = Scraper()  # define Scraper
        self.db = db  # define database

        # on build

    # interval execute core process process function
    def mining(self, time, urls=[]):
        if time - self.run_timed > self.delay:
            self.run_timed = time
            t = Thread(target=self.__process, args=(urls,))
            t.start()

    # <| Private Function |>
    # core process function
    def __process(self, urls=[]):
        for url in urls:
            text = self.scraper.scraping(
                url=url, value='//*[@class="post-content"]')
