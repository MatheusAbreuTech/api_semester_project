from flask import jsonify

class AlunoModel:
    def __init__(self):
        self.alunos = [
                {"id": 1, "nome": "João Pereira", "idade": 15, "turma_id": 1},
                {"id": 2, "nome": "Mariana Lima", "idade": 14, "turma_id": 1},
                {"id": 3, "nome": "Lucas Oliveira", "idade": 16, "turma_id": 2},
                {"id": 4, "nome": "Beatriz Santos", "idade": 15, "turma_id": 2},
                {"id": 5, "nome": "Gabriel Martins", "idade": 14, "turma_id": 2}
            ]

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
            "alunos": self.alunos
        })