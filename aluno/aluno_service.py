from aluno.aluno_model import Aluno
from app import db

class AlunoService:
    def valid_data_student(self, data):
        required_fields = ["nome", "idade"]
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"O campo {field} é obrigatório."
        if not isinstance(data["idade"], int) or data["idade"] <= 0:
            return False, "O campo 'idade' deve ser um número inteiro positivo."
        return True, ""

    def create_aluno(self, data):
        valid, message = self.valid_data_student(data)
        if not valid:
            return {"erro": message}, 400

        aluno = Aluno(
            nome = data["nome"],
            idade = data["idade"],
            turma_id = None
        )

        db.session.add(aluno)
        db.session.commit()

        return {
            "message": "Aluno criado com sucesso!",
            "aluno": aluno
        }

    def get_alunos(self):
        aluno = Aluno.query.all()
        return aluno.to_json(), 200

    def get_aluno(self, aluno_id):
        aluno = Aluno.query.get_or_404(aluno_id)
        return aluno.to_json(), 200

    def update_aluno(self, aluno_id, data):
        for aluno in self.alunos:
            if aluno['id'] == aluno_id:

                valid, message = self.valid_data_student(data)
                if not valid:
                    return {"erro": message}, 400

                aluno.update(data)

                return {
                    "message": "Aluno atualizado com sucesso!",
                    "alunos": self.alunos
                }, 200

        return {"error": "aluno não encontrado"}, 404

    def delete_aluno(self, aluno_id):
        for aluno in self.alunos:
            if aluno['id'] == aluno_id:
                self.alunos.remove(aluno)
                return {"message": "Aluno deletado com sucesso!"}, 200
        return {"error": "aluno não encontrado"}, 404