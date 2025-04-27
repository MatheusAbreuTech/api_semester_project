from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base


db = SQLAlchemy()


Base = declarative_base()


class BaseModel(db.Model):

    __abstract__ = True
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
        
    @classmethod
    def get_all(cls):
        return cls.query.all()
        
    def get_by_id(cls, id):
        return cls.query.get(id)
