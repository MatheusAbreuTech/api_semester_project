from database.db import db
from dataclasses import dataclass


@dataclass
class Turma(db.Model):
    __tablename__= 'turma'


    id:int = db.Column(db.Integer, primary_key=True)
    nome: str = db.Column(db.String(100), nullable=False)
    professor_id: int = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    
    def __init__(self, nome: str):
        self.nome = nome

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

    def __repr__(self):
        return f"<Turma {self.nome}>"

    def to_json(self):
        return {'id': self.id,
                'nome': self.nome
        }
            


    