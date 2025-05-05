from aluno.aluno_model import Aluno
from database.db import db
from sqlalchemy.exc import SQLAlchemyError

class AlunoService:
    def create_aluno(self, data):
        try:
            if not isinstance(data, dict):
                return {"erro": "Dados devem ser um objeto JSON"}, 400
                
            nome = str(data.get('nome', '')).strip()
            idade = data.get('idade')
            turma_id = data.get('turma_id')

            # Validações
            if len(nome) < 3:
                return {"erro": "Nome deve ter pelo menos 3 caracteres"}, 400
                
            try:
                idade = int(idade)
                if idade <= 0:
                    return {"erro": "Idade deve ser maior que zero"}, 400
            except (ValueError, TypeError):
                return {"erro": "Idade deve ser um número válido"}, 400

            # Criação do aluno
            aluno = Aluno(
                nome=nome,
                idade=idade,
                turma_id=turma_id
            )
            
            db.session.add(aluno)
            db.session.commit()
            db.session.refresh(aluno)
            
            return {
                "id": aluno.id,
                "nome": aluno.nome,
                "idade": aluno.idade,
                "turma_id": aluno.turma_id
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
                "turma_id": a.turma_id
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
                "turma_id": aluno.turma_id
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
            idade = data.get('idade')
            
            if len(nome) < 3:
                return {"erro": "Nome deve ter pelo menos 3 caracteres"}, 400
                
            try:
                idade = int(idade)
                if idade <= 0:
                    return {"erro": "Idade deve ser maior que zero"}, 400
            except (ValueError, TypeError):
                return {"erro": "Idade deve ser um número válido"}, 400

            # Atualização
            aluno.nome = nome
            aluno.idade = idade
            aluno.turma_id = data.get('turma_id')
            
            db.session.commit()
            
            return {
                "id": aluno.id,
                "nome": aluno.nome,
                "idade": aluno.idade,
                "turma_id": aluno.turma_id
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