from flask import jsonify
from database.turmas import turmas
from database.professores import professores


class TurmaModel:
    def __init__(self):
        self.turmas = turmas

    def vald_data_class(self, data):
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

