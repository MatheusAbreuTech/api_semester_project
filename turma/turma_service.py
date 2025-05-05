from flask import jsonify
from database import db
from professor.professor_model import Professor
from sqlalchemy import update
from turma.turma_model import Turma
from aluno.aluno_model import Aluno
from database.db import db
from sqlalchemy.exc import SQLAlchemyError
class TurmaService:
    def valid_data_class(self, data):
        if 'nome' not in data:
            return False, 'nome é um campo obrigatório'
        return True, ''
        
    def get_turmas(self):
        try:
            turmas=Turma.query.all()
            return [turma.to_json() for turma in turmas], 200
        except Exception as e:
            return {"error":f"Erro ao buscar turmas: {str(e)}"}, 500

    def get_turma(self, turma_id):
        try:
            turma = Turma.query.get(turma_id)
            if not turma:
                return {'error': 'turma nao encontrada'}, 404
            return turma.to_json(), 200
        except Exception as e:
            return {"error":f"Erro ao buscar turma: {str(e)}"}, 500
        
    def create_turma(self, data):
        
        try:
            if not isinstance(data, dict):
                return {'error': 'Dados inválidos'}, 400 
            
            nome=data.get('nome')
            if not nome:
                return {'error': 'O campo nome é obrigatório'}, 400
            
            turma = Turma.query.filter_by(nome=nome).first()
            if turma:
                return {'error': 'turma ja cadastrada'}, 400

            turma = Turma(
                nome=nome
            )

            db.session.add(turma)
            db.session.commit()
            db.session.refresh(turma)
            return {
                'message': 'turma criada com sucesso',
                'turma': {
                    'id': turma.id,
                    'nome': turma.nome
                }
            }, 201
        except SQLAlchemyError as e:
            # db.session.rollback()
            return {"erro": f"Erro no banco de dados: {str(e)}"}, 500
        except Exception as e:
            # db.session.rollback()
            return {"erro": f"Erro inesperado: {str(e)}"}, 500
        
    def update_turma(self, turma_id, data):
        try:
            turma = Turma.query.get(turma_id)
            if not turma:
                return {'error': 'turma nao encontrada'}, 404
            
            turma.nome=data['nome']
            
            db.session.commit()
            return {
                'message': 'turma atualizada com sucesso',
                'turma': turma.to_json()
            }, 200
        except SQLAlchemyError as e:
            # db.session.rollback()
            return {"erro": f"Erro ao atualizar professor: {str(e)}"}, 400

    def delete_turma(self, turma_id):
        try:
            turma = Turma.query.get(turma_id)
            if not turma:
                return {'error': 'turma nao encontrada'}, 404
            db.session.delete(turma)
            db.session.commit()
            return {'message': 'turma deletada com sucesso'}, 200
        except Exception as e:
            # db.session.rollback()
            return {'error': f'Erro ao deletar turma: {str(e)}'}, 500
        
    def add_student(self, turma_id, aluno_id):
        try:
            query=(
               update(Aluno)
               .where(id == aluno_id)
               .values(turma_id=turma_id)
            )

            aluno=Aluno.query.get(aluno_id)
            if not aluno:
                return {'error': 'aluno nao encontrado'}, 404
            turma = Turma.query.get(turma_id)
            if not turma:
                return {'error': 'turma nao encontrada'}, 404
            if turma_id in aluno.to_json()['turma_id']:  # Verifica se o aluno ja esta na turma
                return {'error': 'aluno ja esta na turma'}, 400
            db.session.execute(query)
            db.session.commit()
            return {'message': 'aluno adicionado a turma com sucesso'}, 200
        except Exception as e:
            # db.session.rollback()
            return {'error': f'Erro ao adicionar aluno a turma: {str(e)}'}, 500

            
    def remove_student(self, turma_id, aluno_id):
       try:
            query=(
               update(Aluno)
               .where(Aluno.id == aluno_id)
               .values(turma_id=None)
            )

            aluno=Aluno.query.get(aluno_id)
            if not aluno:
                return {'error': 'aluno nao encontrado'}, 404
            turma = Turma.query.get(turma_id)
            if not turma:
                return {'error': 'turma nao encontrada'}, 404
            db.session.execute(query)
            db.session.commit()
            return{'message': 'Aluno removido com sucesso'}
       except Exception as e:
            # db.session.rollback()
            return {'error': f'Erro ao remover aluno: {str(e)}'}, 500

    def add_professor(self, turma_id, professor_id):
        try:
            professor=Professor.query.get(professor_id)
            if not professor:
                return {'error': 'Professor nao encontrado'}, 404
            turma=Turma.query.get(turma_id)
            
            if not turma:
                return {'error': 'turma nao encontrada'}, 404
            
            if turma.to_json()['professor_id'] is not None:  # Verifica se o professor ja esta na turma
                return {'error': 'Já existe um professor na turma'}, 400
            
            query = update(Turma).where(Turma.id == turma_id).values(professor_id=professor_id)
            db.session.execute(query)
            db.session.refresh(turma)
            db.session.commit()
            return {'message': 'Professor adicionado a turma com sucesso', 'turma': turma.to_json()}, 200
        except Exception as e:
            # db.session.rollback()
            return {'error': f'Erro ao adicionar Professor a turma: {str(e)}'}, 500
        
    def remove_professor(self, turma_id, professor_id):
        try:
                query=(
                    update(Turma)
                    .where(Turma.id == turma_id)
                    .values(professor_id=None)
                )

                professor=Professor.query.get(professor_id)
                if not professor:
                    return {'error': 'professor nao encontrado'}, 404
                turma = Turma.query.get(turma_id)
                if not turma:
                    return {'error': 'turma nao encontrada'}, 404
                db.session.execute(query)
                db.session.refresh(turma)
                db.session.commit()
                return{'message': 'Professor removido com sucesso'},200
        except Exception as e:
                # db.session.rollback()
                return {'error': f'Erro ao remover aluno: {str(e)}'}, 500