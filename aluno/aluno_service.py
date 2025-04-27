from aluno.aluno_model import Aluno
from database.db import db
from sqlalchemy.exc import SQLAlchemyError

class AlunoService:
    @staticmethod
    def valid_data_student(self, data):
        required_fields = ["nome", "idade"]
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"O campo {field} é obrigatório."
            
        try:
            idade = int(data["idade"])
            if idade <= 0:
                return False, "A idade deve ser um número inteiro positivo."
        except (ValueError, TypeError):
            return False, "A idade deve ser um número inteiro válido."

        return True, ""

    def create_aluno(self, data):
        valid, message = self.valid_data_student(data)
        if not valid:
            return {"erro": message}, 400
        
        try:
            aluno = Aluno(
                nome = data["nome"],
                idade = data["idade"],
                turma_id = data.get("turma_id")
            )

            db.session.add(aluno)
            db.session.commit()

            return {
                "message": "Aluno criado com sucesso!",
                "aluno": aluno.to_json()
            }, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"erro": f"Erro ao criar aluno: {str(e)}"}, 500

    def get_alunos(self):
        try:
            alunos = Aluno.query.all()
            return [aluno.to_json() for aluno in alunos], 200
        except SQLAlchemyError as e:
            return {"erro": f"Erro ao buscar alunos: {str(e)}"}, 500

    def get_aluno(self, aluno_id):
        try:
            aluno = Aluno.query.get(aluno_id)
            if not aluno:
                return {"erro": "Nenhum aluno encontrado"}, 404
            return aluno.to_json(), 200
        except SQLAlchemyError as e:
            return {"erro": f"Erro ao buscar aluno: {str(e)}"}, 500

    def update_aluno(self, aluno_id, data):
        try:
            aluno = Aluno.query.get(aluno_id)
            if not aluno:
                return {"erro": "Nenhum aluno encontrado"}, 404

            valid, message = self.valid_data_student(data)
            if not valid:
                return {"erro": message}, 400

            aluno.nome = data["nome"]
            aluno.idade = int(data["idade"])

            if "turma_id" in data:
                aluno.turma_id = data["turma_id"]

            db.session.commit()

            return {
                "message": "Aluno atualizado com sucesso!",
                "aluno": aluno.to_json()
            }, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"erro": f"Erro ao atualizar aluno: {str(e)}"}, 500

    def delete_aluno(self, aluno_id):
        try:
            aluno = Aluno.query.get(aluno_id)
            if not aluno:
                return {"erro": "Nenhum aluno encontrado"}, 404
            
            db.session.delete(aluno)
            db.session.commit()
            return {"message": "Aluno deletado com sucesso!"}, 200
        except SQLAlchemyError as e:
            return {"erro": f"Erro ao deletar aluno: {str(e)}"}, 500