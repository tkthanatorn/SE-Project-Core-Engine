import psycopg2 as pg
from src.utils import Log


class Postgresql:
    def __init__(self, host, dbname, port, username, password) -> None:
        dns = f"host={host} port={port} user={username} password={password} dbname={dbname}"
        self.conn = pg.connect(dns)
        print("SQL Connected...")

    @Log('Postgresql')
    def execute(self, command: str):
        cur = self.conn.cursor()
        cur.execute(command)
        return cur

    @Log('Postgresql')
    def execute_commit(self, command: str):
        cur = self.conn.cursor()

        cur.execute(command)
        self.conn.commit()

        cur.close()
