from sqlalchemy.orm import Session
from src.model import SourceConfigs


class SourceConfigDatabase:
    def __init__(self, db: Session):
        self.db: Session = db
    
    
    def save(self, source_config: SourceConfigs):
        data = self.db.query(SourceConfigs).filter(SourceConfigs.source == source_config.source).first()
        if data == None:
            self.db.add(source_config)
            self.db.commit()
    
    def all(self) -> list[SourceConfigs]:
        data = self.db.query(SourceConfigs).all()
        return data