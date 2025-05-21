
from database.db import db
from dataclasses import dataclass

@dataclass
class Professor(db.Model):
    __tablename__ = 'professores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    observacoes=db.Column(db.String(250), nullable=True)

    def __init__(self, nome, materia,idade,observacoes):
        self.nome = nome
        self.materia = materia
        self.idade=idade
        self.observacoes=observacoes

    def __repr__(self):
        return f"<Professor {self.nome}, Nome: {self.nome}, Materia: {self.materia}, Idade:{self.idade}, Obs:{self.observacoes}>"
    
    def to_json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "materia": self.materia,
            "idade": self.idade,
            "obs":self.observacoes
        }






