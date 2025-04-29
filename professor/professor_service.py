from flask import jsonify, request
from database.professores import professores

class ProfessorService:
    def __init__(self):
        self.professores = professores

    def create_professor(self, data):
        valid, message = self.valid_data_professor(data)
        if not valid:
            return {"erro": message}, 400
        
        try:
            professor = Professor(
                id = data["id"],
                nome = data["nome"],
                disciplina = data["disciplina"],
                turma_id = data["turma_id"]
            )
            
            db.session.add(professor)
            db.session.commit()

            return {
                "message": "Professor criado com sucesso!",
                "professor": professor.to_json()
            }, 201
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return{"erro": f"Erro ao criar professor: {str(e)}"}, 500

    def get_professor(self):
        try:
            professor = Professor.query.get(professor_id)
            if not professor:
                return {"erro": "Nenhum professor encontrado"}, 404
            return professor.to_json(), 200
        except SQLAlchemyError as e:
            return {"erro": f"Erro ao buscar : {str(e)}"}, 500

    def get_professores(self):
        try:
            professor =  Professor.query.all()
            return [professor.to_json() for professor in professores], 200
        except SQLAlchemyError as e:
            return {"erro": f"Erro ao buscar professor: {str(e)}"}, 500


    def update_professor(self,professor_id,data):
        try:
            professor = Professor.query.get(professor_id)
            if not professor:
                return {"erro": message}, 404
            
            professor.nome = data["nome"]
            professor.disciplina = data["disciplina"]
            
            if "turma_id" in data:
                professor.turma_id = data["turma_id"]
                
            db.session.commit()
            
            return {
                "message": "Professor atualizado com sucesso!",
                "professor": professor.to_json()
            }, 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"erro": f"Erro ao atualizar professor: {str(e)}"}, 500
            
    def delete_professor(self,professor_id):
        try:
            professor = Professor.query.get(professor_id)
            if not professor:
                return {"erro": "Nenhum professor encontrado"}, 404
            
            db.session.delete(professor)
            db.session.commit()
            return {"message": "Professor deletado com sucesso!"}, 200
        except SQLAlchemyError as e:
            return {"erro": f"Erro ao deletar professor: {str(e)}"}, 500
