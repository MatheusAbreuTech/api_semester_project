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


if __name__ == '__main__':
    unittest.main()
