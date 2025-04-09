from flask import jsonify

from database.alunos import alunos
from database.turmas import turmas
from database.professores import professores


class TurmaModel:
    def __init__(self):
        self.turmas = turmas

    def valid_data_class(self, data):
        if 'nome' not in data:
            return False, 'nome é um campo obrigatório'
        if 'id_professor' not in data:
            return False, 'id_professor é um campo obrigatório'

        if not any(p['id'] == data['id_professor'] for p in professores):
            return False, f'professor {data["id_professor"]} nao encontrado'

        return True, ''

    def get_turmas(self):
        return jsonify({'turmas': self.turmas})

    def get_turma(self, turma_id):
        for turma in self.turmas:
            if turma['id'] == turma_id:
                return jsonify({'turma': turma}), 200
        return jsonify({'error': 'turma nao encontrada'}), 404

    def create_turma(self, data):
        valid, msg = self.valid_data_class(data)
        if not valid:
            return jsonify({'error': msg}), 400

        turma = {
            'id': len(self.turmas) + 1,
            'nome': data['nome'],
            'id_professor': data['id_professor']
        }
        self.turmas.append(turma)
        return jsonify({
            'message': 'turma criada com sucesso',
            'turma': turma
        }), 200

    def update_turma(self, turma_id, data):
        for turma in self.turmas:
            if turma['id'] == turma_id:
                valid, msg = self.valid_data_class(data)
                if not valid:
                    return jsonify({'error': msg}), 400

                turma.update(data)
                return jsonify({
                    'message': 'turma atualizada com sucesso',
                    'turma': turma
                }), 200
        return jsonify({'error': 'turma nao encontrada'}), 404

    def delete_turma(self, turma_id):
        for turma in self.turmas:
            if turma['id'] == turma_id:
                self.turmas.remove(turma)
                return jsonify({'message': 'turma removida com sucesso'})
        return jsonify({'error': 'turma nao encontrada'}), 404

    def add_student_in_the_class(self, turma_id, aluno_id):
        aluno = next((a for a in alunos if a['id'] == aluno_id), None)
        turma = next((t for t in turmas if t['id'] == turma_id), None)

        if not aluno:
            return jsonify({'error': 'aluno nao encontrado'}), 404
        if not turma:
            return jsonify({'error': 'turma nao encontrado'}), 404

        aluno["turma_id"] = turma_id
        return jsonify({'message': f'aluno cadastrado com sucesso na turma {turma_id}'})
