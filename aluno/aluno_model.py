from database.db import db
from dataclasses import dataclass

@dataclass
class Aluno(db.Model):
    __tablename__ = 'alunos'

    id:int = db.Column(db.Integer, primary_key=True)
    nome: str = db.Column(db.String(100), nullable=False)
    idade: int = db.Column(db.Integer, nullable=False)
    turma_id: int = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=True)

    def __init__(self, nome: str, idade: int, turma_id: int = None):
        self.nome = nome
        self.idade = idade
        self.turma_id = turma_id

    def __repr__(self):
        return f"<Aluno {self.nome}, Idade: {self.idade}, Turma: {self.turma_id}>"
    
    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'turma_id': self.turma_id
        }