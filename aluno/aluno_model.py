from database.db import db
from dataclasses import dataclass
from datetime import date

@dataclass
class Aluno(db.Model):
    __tablename__ = 'alunos'

    id:int = db.Column(db.Integer, primary_key=True)
    nome: str = db.Column(db.String(100), nullable=False)
    idade: int = db.Column(db.Integer, nullable=False)
    turma_id: int = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=True)
    data_nasc: date = db.Column(db.Date, nullable=False)
    nota_semestre1: float=db.Column(db.Float,nullable=False)
    nota_semestre2: float=db.Column(db.Float,nullable=False) 
    media_final: float=db.Column(db.Float,nullable=False)    

    def __init__(self, nome: str, idade: int, turma_id: int = None, data_nasc:date, nota_semestre1:float, nota_semestre2:float):
        self.nome = nome
        self.idade = idade
        self.turma_id = turma_id
        self.data_nasc=data_nasc
        self.nota_semestre1=nota_semestre1
        self.nota_semestre2=nota_semestre2


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
        return f"<Aluno id: {self.id}, nome: {self.nome}, idade: {self.idade},turma_id: {self.turma_id}, data de nascimento:{self.data_nasc},Nota 1º semestre:{self.nota_semestre1},Nota 2° semestre{self.nota_semestre2},Media_final:{self.media_final}>"
    
    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'turma_id': self.turma_id,
            'data_nasc':self.data_nasc,
            'nota_semestre1':self.nota_semestre1,
            'nota_semestre2':self.nota_semestre2,
            'media_final':self.media_final
        }