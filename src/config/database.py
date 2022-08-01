from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.pool import QueuePool
import os


_USER = os.environ.get("DB_USER")
_PASSWORD = os.environ.get("DB_PASSWORD")
_HOST = os.environ.get("DB_HOST")
_DBNAME = os.environ.get("DB_NAME")
_DATABASE_URL = f"postgresql://{_USER}:{_PASSWORD}@{_HOST}/{_DBNAME}"


engine = create_engine(_DATABASE_URL, poolclass=QueuePool, pool_size=20)

if not database_exists(engine.url):
    create_database(engine.url)
print("database created: ", database_exists(engine.url))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()