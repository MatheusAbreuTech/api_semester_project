from flask_sqlalchemy import SQLAlchemy
from app import db

class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=True)

    def __init__(self, nome, idade, turma_id):
        self.nome = nome
        self.idade = idade
        self.turma_id = turma_id

    def __repr__(self):
        return f"<Aluno {self.nome}, Idade: {self.idade}, Turma: {self.turma_id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'turma_id': self.turma_id
        }
    
    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'turma_id': self.turma_id
        }