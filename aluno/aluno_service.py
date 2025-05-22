from aluno.aluno_model import Aluno
from database.db import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from datetime import datetime, date

class AlunoService:
    def calcular_idade(self, data_nasc_str):
        data_nasc = datetime.strptime(data_nasc_str, '%Y-%m-%d').date()
        hoje = date.today()
        idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        return idade

    def create_aluno(self, data):
        try:
            if not isinstance(data, dict):
                return {"erro": "Dados devem ser um objeto JSON"}, 400
                
            nome = str(data.get('nome', '')).strip()
            data_nasc = data.get('data_nasc')
            nota_semestre1 = data.get('nota_semestre1')
            nota_semestre2 = data.get('nota_semestre2')

            # Validações
            if len(nome) < 3:
                return {"erro": "Nome deve ter pelo menos 3 caracteres"}, 400
                
            if ((nota_semestre1 or nota_semestre2) is None):
                return{"erro": 'As notas são campos obrigatorio'},400  

            media_final = (nota_semestre1 + nota_semestre2)/2
            

            # Criação do aluno
            aluno = Aluno(
                nome=nome,
                idade=self.calcular_idade(data_nasc),
                data_nasc=data_nasc,
                nota_semestre1=nota_semestre1,
                nota_semestre2=nota_semestre2,
                media_final=media_final
            )
            
            db.session.add(aluno)
            db.session.commit()
            db.session.refresh(aluno)
            
            return {
                "id": aluno.id,
                "nome": aluno.nome,
                "idade": aluno.idade,
                "turma_id": aluno.turma_id,
                "data_nasc":str(aluno.data_nasc),
                "nota_semestre1":aluno.nota_semestre1,
                "nota_semestre2":aluno.nota_semestre2,
                "media_final":aluno.media_final
            }, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"erro": f"Erro no banco de dados: {str(e)}"}, 500
        except Exception as e:
            db.session.rollback()
            return {"erro": f"Erro inesperado: {str(e)}"}, 500

    def get_alunos(self):
        try:
            alunos = Aluno.query.all()
            return [{
                "id": a.id,
                "nome": a.nome,
                "idade": a.idade,
                "turma_id": a.turma_id,
                "data_nasc":a.data_nasc,
                "nota_semestre1":a.nota_semestre1,
                "nota_semestre2":a.nota_semestre2,
                "media_final":a.media_final

            } for a in alunos], 200
        except SQLAlchemyError as e:
            return {"erro": f"Erro ao buscar alunos: {str(e)}"}, 500

    def get_aluno(self, aluno_id):
        try:
            aluno = Aluno.query.get(aluno_id)
            if not aluno:
                return {"erro": "Aluno não encontrado"}, 404
                
            return {
                "id": aluno.id,
                "nome": aluno.nome,
                "idade": aluno.idade,
                "turma_id": aluno.turma_id,
                "data_nasc":aluno.data_nasc,
                "nota_semestre1":aluno.nota_semestre1,
                "nota_semestre2":aluno.nota_semestre2,
                "media_final":aluno.media_final

            }, 200
        except SQLAlchemyError as e:
            return {"erro": f"Erro ao buscar aluno: {str(e)}"}, 500

    def update_aluno(self, aluno_id, data):
        try:
            aluno = Aluno.query.get(aluno_id)
            if not aluno:
                return {"erro": "Aluno não encontrado"}, 404

            # Validações
            nome = str(data.get('nome', '')).strip()
            data_nasc = data.get('data_nasc')
            nota_semestre1 = data.get('nota_semestre1')
            nota_semestre2 = data.get('nota_semestre2')

            # Validações
            if len(nome) < 3:
                return {"erro": "Nome deve ter pelo menos 3 caracteres"}, 400
                
            if ((nota_semestre1 or nota_semestre2) is None):
                return{"erro": 'As notas são campos obrigatorio'},400  

            media_final = (nota_semestre1 + nota_semestre2)/2

            # Atualização
            aluno.nome = nome
            aluno.idade = self.calcular_idade(data_nasc)
            aluno.turma_id = data.get('turma_id')
            aluno.data_nasc = data_nasc
            aluno.nota_semestre1 = nota_semestre1
            aluno.nota_semestre2 = nota_semestre2
            aluno.media_final=media_final

            
            db.session.commit()
            
            return {
                "id": aluno.id,
                "nome": aluno.nome,
                "idade": aluno.idade,
                "turma_id": aluno.turma_id,
                "data_nasc": str(aluno.data_nasc),
                "nota_semestre1": aluno.nota_semestre1,
                "nota_semestre2": aluno.nota_semestre2,
                "media_final": aluno.media_final

            }, 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"erro": f"Erro ao atualizar aluno: {str(e)}"}, 500

    def delete_aluno(self, aluno_id):
        try:
            aluno = Aluno.query.get(aluno_id)
            if not aluno:
                return {"erro": "Aluno não encontrado"}, 404
                
            db.session.delete(aluno)
            db.session.commit()
            return "", 204
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"erro": f"Erro ao deletar aluno: {str(e)}"}, 500