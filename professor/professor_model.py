
from database.db import db
from dataclasses import dataclass

@dataclass
class Professor(db.Model):
    __tablename__ = 'professor'

    id:int = db.Column(db.Integer, primary_key=True)
    nome: str = db.Column(db.String(100), nullable=False)
    disciplina: int = db.Column(db.Integer, nullable=False)

    def __init__(self, nome: str, disciplina: str):
        self.nome = nome
        self.disciplina = disciplina

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
        return f"<Professor {self.nome}, Nome: {self.nome}, Disciplina: {self.disciplina}>"
    
    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'disciplina': self.disciplina,
        }






