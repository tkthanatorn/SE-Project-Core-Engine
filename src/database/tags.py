from sqlalchemy.orm import Session

from src.config import SessionLocal
from src.model import Tags


class TagsDatabase:
    def __init__(self, db: Session):
        self.db: Session = db
    
    def save(self, data: Tags):
        self.db.add(data)
        self.db.commit()
    
    def findByName(self, name: str):
        data = self.db.query(Tags).filter(Tags.name == name).first()
        return data
        