from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.config import Base


# News Model
class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, unique=True, nullable=False)
    description = Column(Text)
    url = Column(Text, unique=True, nullable=False)
    icon = Column(String(500))
    source = Column(String(500), nullable=False)
    major_url = Column(String(100), nullable=False)
    minor_url = Column(String)
    text = Column(Text)
    polarity = Column(Float)
    sentiment = Column(String(32))
    date = Column(DateTime)
    tags = relationship('Tags', secondary='news_tags')


# Tags Model
class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True)
    key = Column(String(64), unique=True)
    symbol = Column(String(32))
    news = relationship('News', secondary='news_tags', overlaps="tags")


# Relation News and Tags Model
class NewsTags(Base):
    __tablename__ = "news_tags"
    id = Column(Integer, primary_key=True)
    news_id = Column(Integer, ForeignKey("news.id"))
    tasgs_id = Column(Integer, ForeignKey("tags.id"))


# Source Config Model
class SourceConfigs(Base):
    __tablename__ = "source_configs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(256), unique=True, nullable=False)
    major_url = Column(String(100), nullable=False)
    minor_url = Column(String(64))
    xpath = Column(String(256))