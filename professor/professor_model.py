from flask import jsonify
from flask import request

from database.professores import professores

class ProfessorModel:
    def __init__(self):
        self.professores = professores

    def create_professor(self, data):
        professor = {
            "id": len(self.professores) + 1,
            "nome": data["nome"],
            "turma_id": None
        }

        self.professores.append(professor)
        return jsonify({
            "message": "Professor criado com sucesso!",
            "professor": professor
        })

    def get_professor(self, professor_id):
        for professor in self.professores:
            if professor["id"] == professor_id:
                return jsonify({"professor": professor}), 200
        return jsonify({'error': 'professor não encontrado'}), 404

    def get_professores(self):
        return jsonify({"professores": self.professores}), 200

    def update_professor(self,professor_id,data):
        for professor in professores:
            if professor['id'] == professor_id:
                data = request.json
                if 'nome' not in data:
                    return jsonify({'error': 'nome é um campo obrigatório'}), 400

                if 'disciplina' not in data:
                    return jsonify({'error': 'disciplina é um campo obrigatório'}), 400

                professor.update(data)
                return jsonify({
                    'message': 'professor atualizado com sucesso',
                    'professor': professor
                })

        return jsonify({'error': 'professor nao encontrado'}), 404
    
    def delete_professor(self,professor_id):
        for professor in professores:
            if professor['id'] == professor_id:
                professores.remove(professor)
                return jsonify({
                    'message': 'professor removido com sucesso'
                })

        return jsonify({'error': 'professor nao encontrado'}), 404





