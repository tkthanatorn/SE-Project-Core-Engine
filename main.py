from datetime import datetime
import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
load_dotenv(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".dev.env"))

from src.core.luancher import luancher
from src.command import Fetch
from src.database import NewsDatabase, TagsDatabase
from src.model import Tags, News
from src.config import SessionLocal

if __name__ == "__main__":
    luancher()