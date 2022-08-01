from datetime import datetime, timedelta
from threading import Thread
from sqlalchemy.orm import Session

from src.config import get_config
from src.command import Miner
from src.util.logging import log_info

class MinerController:
    def __init__(self, db: Session):
        self.execute_time = datetime.now().timestamp()
        self.delay = int(get_config(['interval_config', 'miner_delay']))
        self.miner = Miner(db)
    
    def luanch(self, time: float):
        if self.execute_time <= time:
            log_info("mining...")

            self._increment_execute_time()
            worker_cryptorank = Thread(target=self.miner.mining_cryptorank)
            worker_cryptorank.start()

    def _increment_execute_time(self):
        self.execute_time = (datetime.fromtimestamp(self.execute_time) + timedelta(minutes=self.delay)).timestamp()