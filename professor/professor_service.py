from flask import jsonify, request
from database.db import db
from professor.professor_model import Professor
from sqlalchemy.exc import SQLAlchemyError

class ProfessorService:
    def create_professor(self, data):
        try:
            if not isinstance(data, dict):
                return {"erro": "Formato de dados inválido"}, 400

            nome = data.get('nome', '').strip()
            materia = data.get('materia', '').strip()
            idade=data.get('idade')
            observacoes=data.get('observacoes', '').strip()

            if len(nome) < 3:
                return {"erro": "Nome deve ter pelo menos 3 caracteres"}, 400
            if len(materia) < 1:
                return {"erro": "Disciplina é obrigatória"}, 400
            if idade < 18:
                return{"erro":"Tu num é muito jovem pra dar aula?"}, 400
            
            professor = Professor(
                nome=nome,
                materia=materia,
                idade=idade,
                observacoes=observacoes
            )
            
            db.session.add(professor)
            db.session.commit()
            db.session.refresh(professor)
            
            return {
                "id": professor.id,
                "nome": professor.nome,
                "materia": professor.materia,
                "idade":professor.idade,
                "observacoes":professor.observacoes
            }, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"erro": f"Erro no banco de dados: {str(e)}"}, 500
        except Exception as e:
            db.session.rollback()
            return {"erro": "Erro interno ao processar a requisição"}, 500
    
    def get_professor(self, professor_id):
        try:
            professor = Professor.query.get(professor_id)
            if not professor:
                return {"erro": "Nenhum professor encontrado"}, 404
            return professor.to_json(), 200
        except SQLAlchemyError as e:
            return {"erro": f"Erro ao buscar professor: {str(e)}"}, 500

    def get_professores(self):
        try:
            professores = Professor.query.all()
            return [professor.to_json() for professor in professores], 200
        except SQLAlchemyError as e:
            return {"erro": f"Erro ao buscar professores: {str(e)}"}, 500

    def update_professor(self, professor_id, data):
        print(data)
        if "nome" not in data or "materia" not in data or "idade" not in data:
            return {"erro": "Todos os campos são obrigatórios"}, 400
            
        try:
            professor = Professor.query.get(professor_id)
            if not professor:
                return {"erro": "Nenhum professor encontrado"}, 404
            
            professor.nome = data["nome"]
            professor.materia = data["materia"]
            professor.idade=data["idade"]
            professor.observacoes=data["observacoes"]
                
            db.session.commit()
            
            return {
                "message": "Professor atualizado com sucesso!",
                "professor": professor.to_json()
            }, 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"erro": f"Erro ao atualizar professor: {str(e)}"},400
        except Exception as e:
            db.session.rollback()
            return {"erro": "Erro interno ao processar a requisição"}, 500
            
    def delete_professor(self, professor_id):
        try:
            professor = Professor.query.get(professor_id)
            if not professor:
                return {"erro": "Nenhum professor encontrado"}, 404
            
            db.session.delete(professor)
            db.session.commit()
            return {"message": "Professor deletado com sucesso!"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"erro": f"Erro ao deletar professor: {str(e)}"}, 500