from database.turmas import turmas
from database.professores import professores


class TurmaModel:
    def __init__(self):
        self.turmas = turmas

    def validar_dados_turma(self, data):
        if 'nome' not in data:
            return False, 'nome é um campo obrigatório'
        if 'id_professor' not in data:
            return False, 'id_professor é um campo obrigatório'

        if not any(p['id'] == data['id_professor'] for p in professores):
            return False, f'professor {data["id_professor"]} nao encontrado'

        return True, ''
