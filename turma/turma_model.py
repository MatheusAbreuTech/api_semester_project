from database.db import db
from dataclasses import dataclass

@dataclass
class Turma(db.Model):
    __tablename__= 'turmas'

    id:int = db.Column(db.Integer, primary_key=True)
    descricao: str = db.Column(db.String(100), nullable=False)
    professor_id: int = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=True)
    ativo: bool = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, descricao: str, professor_id: int = None,     ativo: bool = True ):
        self.descricao = descricao
        self.ativo = ativo
        self.professor_id = professor_id

    def __repr__(self):
        return f"<Turma id: {self.id}, descricao: {self.descricao} professor_id: {self.professor_id} ativo: {self.ativo}>"

    def to_json(self):
        return {'id': self.id,
                'descricao': self.descricao,
                'professor_id': self.professor_id,
                'ativo': self.ativo
                
        }