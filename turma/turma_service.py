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
        if 'descricao' not in data:
            return False, 'descricao é um campo obrigatório'
        elif 'ativo' not in data:
            return False,  'Disponibilidade da turma é um campo obrigatorio'
        return True, ''
        
    def get_turmas(self):
        try:
            turmas=Turma.query.filter_by(ativo=True).all()
            return [turma.to_json() for turma in turmas], 200
        except SQLAlchemyError as e:
            return {"error":f"Erro ao buscar turmas: {str(e)}"}, 500

    def get_turma(self, turma_id):
        try:
            turma = Turma.query.get(turma_id)
            if not turma or not turma.ativo:
                return {'error': 'turma nao encontrada'}, 404
            return turma.to_json(), 200
        except SQLAlchemyError as e:
            return {"error":f"Erro ao buscar turma: {str(e)}"}, 500
        
    def create_turma(self, data):
        try:
            valid, message = self.valid_data_class(data)
            if not valid:
                return {'error': message}, 400
            
            descricao = data.get('descricao')
            professor_id = data.get('professor_id')
            
            if professor_id and not Professor.query.get(professor_id):
                return {'error': 'professor nao encontrado'}, 404
            
            turma = Turma.query.filter_by(descricao=descricao).first()
            if turma:
                return {'error': 'turma ja cadastrada'}, 400

            turma = Turma(
                descricao=descricao,
                professor_id=professor_id,
                ativo=data.get('ativo', True)
            )

            db.session.add(turma)
            db.session.commit()
            db.session.refresh(turma)
            return {
                'message': 'turma criada com sucesso',
                'turma': turma.to_json()
            }, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"erro": f"Erro no banco de dados: {str(e)}"}, 500
        except Exception as e:
            db.session.rollback()
            return {"erro": f"Erro inesperado: {str(e)}"}, 500
        
    def update_turma(self, turma_id, data):
        try:
            turma = Turma.query.get(turma_id)
            if not turma or not turma.ativo:
                return {'error': 'turma nao encontrada'}, 404
            
            if 'descricao' in data:
                turma.descricao = data['descricao']

            if 'ativo' in data:
                turma.ativo = data['ativo']    

            if 'professor_id' in data:
                if data['professor_id'] and not Professor.query.get(data['professor_id']):
                    return {'error': 'professor nao encontrado'}, 404
                turma.professor_id = data['professor_id']
            
            db.session.commit()
            return {
                'message': 'turma atualizada com sucesso',
                'turma': turma.to_json()
            }, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"erro": f"Erro ao atualizar professor: {str(e)}"}, 400

    def delete_turma(self, turma_id):
        try:
            turma = Turma.query.get(turma_id)
            if not turma:
                return {'error': 'turma nao encontrada'}, 404
            
            # turma.ativo = False
            db.session.delete(turma)
            db.session.commit()

            return {'message': 'turma deletada com sucesso'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'Erro ao deletar turma: {str(e)}'}, 500
        
    def _get_turma_and_aluno(self, turma_id, aluno_id):
        turma = Turma.query.get(turma_id)
        if not turma or not turma.ativo:
            return None, None, {'error': 'Turma não encontrada ou inativa'}, 404
            
        aluno = Aluno.query.get(aluno_id)
        if not aluno or not aluno.ativo:
            return None, None, {'error': 'Aluno não encontrado ou inativo'}, 404
            
        return turma, aluno, None, None

    def add_student(self, turma_id, aluno_id):
        try:
            turma, aluno, error, status = self._get_turma_and_aluno(turma_id, aluno_id)
            if error:
                return error, status
                
            if aluno.turma_id == turma_id:
                return {'error': 'Aluno já está nesta turma'}, 400
                
            if aluno.turma_id:
                return {'error': 'Aluno já está em outra turma'}, 400
                
            aluno.turma_id = turma_id
            db.session.commit()
            
            return {'message': 'Aluno adicionado à turma com sucesso'}, 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': f'Erro ao adicionar aluno à turma: {str(e)}'}, 500
            
    def remove_student(self, turma_id, aluno_id):
        try:
            turma, aluno, error, status = self._get_turma_and_aluno(turma_id, aluno_id)
            if error:
                return error, status
                
            if aluno.turma_id != turma_id:
                return {'error': 'Aluno não está nesta turma'}, 400
                
            aluno.turma_id = None
            db.session.commit()
            
            return {'message': 'Aluno removido da turma com sucesso'}, 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': f'Erro ao remover aluno da turma: {str(e)}'}, 500
        
    def _get_turma_and_professor(self, turma_id, professor_id):
        """Método auxiliar para obter turma e professor com validações"""
        turma = Turma.query.get(turma_id)
        if not turma or not turma.ativo:
            return None, None, {'error': 'Turma não encontrada ou inativa'}, 404
            
        professor = Professor.query.get(professor_id)
        if not professor or not professor.ativo:
            return None, None, {'error': 'Professor não encontrado ou inativo'}, 404
            
        return turma, professor, None, None

    def add_professor(self, turma_id, professor_id):        
        try:
            turma, professor, error, status = self._get_turma_and_professor(turma_id, professor_id)
            if error:
                return error, status
                
            if turma.professor_id == professor_id:
                return {'error': 'Este professor já está associado à turma'}, 400
                
            if turma.professor_id:
                return {'error': 'Já existe um professor associado à turma'}, 400
                
            turma.professor_id = professor_id
            db.session.commit()
            
            return {
                'message': 'Professor associado à turma com sucesso',
                'turma': turma.to_json()
            }, 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': f'Erro ao associar professor à turma: {str(e)}'}, 500
        
    def remove_professor(self, turma_id, professor_id):
        try:
            turma, professor, error, status = self._get_turma_and_professor(turma_id, professor_id)
            if error:
                return error, status
                
            if turma.professor_id != professor_id:
                return {'error': 'Este professor não está associado à turma'}, 400
                
            turma.professor_id = None
            db.session.commit()
            
            return {
                'message': 'Professor removido da turma com sucesso',
                'turma': turma.to_json()
            }, 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': f'Erro ao remover professor da turma: {str(e)}'}, 500