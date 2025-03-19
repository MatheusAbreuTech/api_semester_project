import unittest

from flask import json
from app import app, alunos


class TestAPP(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_alunos(self):
        response = self.app.get('/alunos')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

    def test_get_aluno_existente(self):
        response = self.app.get('/alunos/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('aluno', json.loads(response.data))

    def test_get_aluno_inexistente(self):
        response = self.app.get('/alunos/999')
        self.assertEqual(response.status_code, 404)

    def test_create_aluno(self):
        novo_aluno = {
            "nome": "Teste Aluno",
            "idade": 17,
            "turma_id": 1
        }
        response = self.app.post('/alunos', data=json.dumps(novo_aluno), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', json.loads(response.data))

    def test_create_aluno_dados_invalidos(self):
        aluno_invalido = {
            "nome": "Sem Idade"
        }
        response = self.app.post('/alunos', json=aluno_invalido)
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.data)
        self.assertIn("erro", data)

    def test_update_aluno_existente(self):
        update_data = {"nome": "João Modificado", "idade": 16, "turma_id": 1}
        response = self.app.put('/alunos/1', json=update_data)
        self.assertEqual(response.status_code, 200)

    def test_update_aluno_inexistente(self):
        update_data = {"nome": "Nome Inválido", "idade": 18, "turma_id": 2}
        response = self.app.put('/alunos/999', json=update_data)
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)
        self.assertEqual(data["error"], "aluno não encontrado")

    def test_delete_aluno_existente(self):
        response = self.app.delete('/alunos/2')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["message"], "Aluno deletado com sucesso!")

    def test_delete_aluno_inexistente(self):
        response = self.app.delete('/alunos/999')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)
        self.assertEqual(data["error"], "aluno não encontrado")

    def test_get_professor_existente(self):
        response = self.app.get('/professor/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["professor"]["nome"], "Ana Silva")

    def test_get_professor_inexistente(self):
        response = self.app.get('/professor/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "professor nao encontrado")

if __name__ == '__main__':
    unittest.main()
