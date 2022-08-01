from sqlalchemy import func, asc, and_
from sqlalchemy.orm import Session

from src.model import News, NewsTags


class NewsDatabase:
    def __init__(self, db: Session):
        self.db: Session = db
    
    def save(self, data: News):
        self.db.add(data)
        self.db.commit()
    
    def all(self) -> list:
        return self.db.query(News).all()
    
    def latest_news_date(self):
        return self.db.query(func.max(News.date)).first()[0]
    
    def update(self, id: int, data: dict):
        news = self.db.query(News).filter(News.id == id).update(data)
        self.db.commit()
    
    def delete(self, id: int):
        self.db.query(NewsTags).filter(NewsTags.news_id == id).delete()
        self.db.query(News).filter(News.id == id).delete()
        self.db.commit()
    
    def get_null_text(self, limit: int=100) -> list[News]:
        data = self.db.query(News).filter(News.text.is_(None)).order_by(asc(News.date)).limit(limit).all()
        return data
    
    def get_null_sentiment(self, limit: int=100) -> list[News]:
        data = self.db.query(News).filter(and_(News.text.is_not(None), News.sentiment.is_(None))).order_by(asc(News.date)).limit(limit).all()
        return data
        