from flask import jsonify, request
from professor_model import Professor

class ProfessorService:
    def create_professor(self, data):
        if "nome" not in data:
            return {"erro": "O campo 'nome' é obrigatório"}, 400
        if "disciplina" not in data:
            return {"erro": "O campo 'disciplina' é obrigatório"}, 400
        
        try:
            professor = Professor(
                nome = data["nome"],
                disciplina = data["disciplina"],
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

    def get_professor(self, professor_id):
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
            return {"erro": f"Erro ao buscar professores: {str(e)}"}, 500


    def update_professor(self,professor_id,data):
        try:
            professor = Professor.query.get(professor_id)
            if not professor:
                return {"erro": message}, 404
            
            professor.nome = data["nome"]
            professor.disciplina = data["disciplina"]
                
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
