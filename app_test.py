import unittest
from flask import json
from app import app
from database.alunos import alunos
from database.professores import professores
from database.turmas import turmas

class TestAPP(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        alunos.clear()
        professores.clear()
        turmas.clear()

        alunos.extend([
            {"id": 1, "nome": "João Pereira", "idade": 15, "turma_id": 1},
            {"id": 2, "nome": "Mariana Lima", "idade": 14, "turma_id": 1},
            {"id": 3, "nome": "Lucas Oliveira", "idade": 16, "turma_id": 2},
            {"id": 4, "nome": "Beatriz Santos", "idade": 15, "turma_id": 2},
            {"id": 5, "nome": "Gabriel Martins", "idade": 14, "turma_id": 3}
        ])

        professores.extend([
            {"id": 1, "nome": "Ana Silva", "disciplina": "Matemática"},
            {"id": 2, "nome": "Carlos Souza", "disciplina": "História"},
            {"id": 3, "nome": "Fernanda Costa", "disciplina": "Biologia"}
        ])

        turmas.extend([
            {"id": 1, "nome": "Turma A", "id_professor": 1},
            {"id": 2, "nome": "Turma B", "id_professor": 2},
            {"id": 3, "nome": "Turma C", "id_professor": 3}
        ])

    def test_get_alunos(self):
        response = self.app.get('/alunos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('alunos', data)
        self.assertEqual(len(data['alunos']), len(alunos))

    def test_get_aluno_existente(self):
        response = self.app.get('/alunos/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('aluno', data)
        self.assertEqual(data['aluno']['id'], 1)

    def test_get_aluno_inexistente(self):
        response = self.app.get('/alunos/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_aluno(self):
        novo_aluno = {"nome": "Teste Aluno", "idade": 17, "turma_id": 1}
        response = self.app.post('/alunos', json=novo_aluno)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('aluno', data)
        self.assertIsInstance(data['aluno'], dict)

    def test_create_aluno_dados_invalidos(self):
        dados_invalidos = [
            {"nome": "Sem Idade"},
            {"idade": 18, "turma_id": 1},
            {"nome": "", "idade": 18, "turma_id": 1},
            {"nome": "Sem Idade", "idade": 0, "turma_id": 1},
            {"nome": "Sem Idade", "idade": -1, "turma_id": 1},
            {"nome": "Sem Idade", "idade": "idade inválida", "turma_id": 1},
        ]
        for dados in dados_invalidos:
            response = self.app.post('/alunos', json=dados)
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertIn('error', data)

    def test_update_aluno_existente(self):
        update_data = {"nome": "João Modificado", "idade": 16, "turma_id": 1}
        response = self.app.put('/alunos/1', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_update_aluno_inexistente(self):
        update_data = {"nome": "Nome Inválido", "idade": 18, "turma_id": 2}
        response = self.app.put('/alunos/999', json=update_data)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_update_aluno_invalido(self):
        update_data = {"nome": "", "idade": 18, "turma_id": 2}
        response = self.app.put('/alunos/1', json=update_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_delete_aluno_existente(self):
        response = self.app.delete('/alunos/2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_delete_aluno_inexistente(self):
        response = self.app.delete('/alunos/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_professor_existente(self):
        response = self.app.get('/professor/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('professor', data)

    def test_get_professor_inexistente(self):
        response = self.app.get('/professor/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_professor(self):
        novo_professor = {"nome": "Paulo Souza", "disciplina": "Física"}
        response = self.app.post('/professor', json=novo_professor)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_update_professor_existente(self):
        update_data = {"nome": "Ana Modificada", "disciplina": "Física"}
        response = self.app.put('/professor/1', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_update_professor_inexistente(self):
        update_data = {"nome": "Nome Inválido", "disciplina": "Química"}
        response = self.app.put('/professor/999', json=update_data)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_delete_professor_existente(self):
        response = self.app.delete('/professor/2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_delete_professor_inexistente(self):
        response = self.app.delete('/professor/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_turma_existente(self):
        response = self.app.get('/turmas/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('turma', data)

    def test_get_turma_inexistente(self):
        response = self.app.get('/turmas/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_turma(self):
        nova_turma = {"nome": "Turma Z", "id_professor": 1}
        response = self.app.post('/turmas', json=nova_turma)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_create_turma_dados_invalidos(self):
        turma_invalida = {"nome": "Turma Sem Professor"}
        response = self.app.post('/turmas', json=turma_invalida)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_update_turma_existente(self):
        update_data = {"nome": "Turma X", "id_professor": 1}
        response = self.app.put('/turmas/1', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_update_turma_existente_professor_inexistente(self):
        update_data = {"nome": "Turma X", "id_professor": 999}
        response = self.app.put('/turmas/1', json=update_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_update_turma_inexistente(self):
        update_data = {"nome": "Turma Z", "id_professor": 1}
        response = self.app.put('/turmas/999', json=update_data)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_delete_turma_existente(self):
        response = self.app.delete('/turmas/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_delete_turma_inexistente(self):
        response = self.app.delete('/turmas/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
