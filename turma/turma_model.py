from database.db import db
from dataclasses import dataclass

@dataclass
class Turma(db.Model):
    __tablename__= 'turmas'

    id:int = db.Column(db.Integer, primary_key=True)
    nome: str = db.Column(db.String(100), nullable=False)
    professor_id: int = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=True)
    
    def __init__(self, nome: str):
        self.nome = nome

    def __repr__(self):
        return f"<Turma id: {self.id}, nome: {self.nome}>"

    def to_json(self):
        return {'id': self.id,
                'nome': self.nome,
                'professor_id': self.professor_id
        }