from flask import jsonify

from database.alunos import alunos

class AlunoModel:
    def __init__(self):
        self.alunos = alunos

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
            return jsonify({"erro": message}), 400

        aluno = {
            "id": len(self.alunos) + 1,
            "nome": data["nome"],
            "idade": data["idade"],
            "turma_id": None
        }

        self.alunos.append(aluno)

        return jsonify({
            "message": "Aluno criado com sucesso!",
            "aluno": aluno
        })

    def get_alunos(self):
        return jsonify({"alunos": self.alunos}), 200

    def get_aluno(self, aluno_id):
        for aluno in self.alunos:
            if aluno["id"] == aluno_id:
                return jsonify({"aluno": aluno}), 200
        return jsonify({"error": "Aluno não encontrado"}), 404

    def update_aluno(self, aluno_id, data):
        for aluno in self.alunos:
            if aluno['id'] == aluno_id:

                valid, message = self.valid_data_student(data)
                if not valid:
                    return jsonify({"erro": message}), 400

                aluno.update(data)

                return jsonify({
                    "message": "Aluno atualizado com sucesso!",
                    "alunos": self.alunos
                }), 200

        return jsonify({"error": "aluno não encontrado"}), 404

    def delete_aluno(self, aluno_id):
        for aluno in self.alunos:
            if aluno['id'] == aluno_id:
                self.alunos.remove(aluno)
                return jsonify({"message": "Aluno deletado com sucesso!"})
        return jsonify({"error": "aluno não encontrado"}), 404