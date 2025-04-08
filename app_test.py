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
        self.assertIsInstance(data, dict)
        self.assertIn('alunos', data)
        self.assertIsInstance(data['alunos'], list)
        self.assertEqual(len(data['alunos']), len(alunos))

    def test_get_aluno_existente(self):
        response = self.app.get('/alunos/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertIn('aluno', data)
        self.assertIsInstance(data['aluno'], dict)
        self.assertEqual(data['aluno']['id'], 1)
        self.assertEqual(data['aluno']['nome'], 'João Pereira')
        self.assertEqual(data['aluno']['idade'], 15)
        self.assertEqual(data['aluno']['turma_id'], 1)

    def test_get_aluno_inexistente(self):
        response = self.app.get('/alunos/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Aluno não encontrado")

    def test_create_aluno(self):
        novo_aluno = {
            "nome": "Teste Aluno",
            "idade": 17,
            "turma_id": 1
        }
        response = self.app.post('/alunos', data=json.dumps(novo_aluno), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Aluno criado com sucesso!')
        self.assertIn('aluno', data)
        self.assertIsInstance(data['aluno'], dict)
        self.assertIn('id', data['aluno'])
        self.assertIsInstance(data['aluno']['id'], int)

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
            self.assertIn("erro", data)

    def test_update_aluno_existente(self):
        update_data = {"nome": "João Modificado", "idade": 16, "turma_id": 1}
        response = self.app.put('/alunos/1', json=update_data)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["message"], "Aluno atualizado com sucesso!")
        self.assertIn("alunos", data)
        self.assertIsInstance(data["alunos"], list)
        aluno = next((a for a in data["alunos"] if a["id"] == 1), None)
        self.assertIsNotNone(aluno)
        self.assertEqual(aluno["nome"], "João Modificado")
        self.assertEqual(aluno["idade"], 16)
        self.assertEqual(aluno["turma_id"], 1)

    def test_update_aluno_inexistente(self):
        update_data = {"nome": "Nome Inválido", "idade": 18, "turma_id": 2}
        response = self.app.put('/alunos/999', json=update_data)
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)
        self.assertEqual(data["error"], "aluno não encontrado")

    def test_update_aluno_invalido(self):
        update_data = {"nome": "", "idade": 18, "turma_id": 2}
        response = self.app.put('/alunos/1', json=update_data)
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.data)
        self.assertIn("erro", data)

    def test_delete_aluno_existente(self):
        quantidade_alunos_inicial = len(alunos)
        response = self.app.delete('/alunos/2')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["message"], "Aluno deletado com sucesso!")

        quantidade_alunos_final = len(alunos) - 1
        self.assertLess(quantidade_alunos_final, quantidade_alunos_inicial)

    def test_delete_aluno_inexistente(self):
        response = self.app.delete('/alunos/999')
        self.assertEqual(response.status_code, 404, "Status code should be 404 for non-existing aluno")

        data = json.loads(response.data)
        self.assertIn("error", data, "Response should contain an 'error' key")
        self.assertEqual(data["error"], "aluno não encontrado", "Error message should be 'aluno não encontrado'")

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

    def test_create_professor(self):
        novo_professor = {
            "nome": "Fernanda Costa",
            "disciplina": "Biologia"
        }
        response = self.app.post('/professor', json=novo_professor)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["message"], "professor criado com sucesso")

    def test_create_professor_dados_invalidos(self):
        professor_invalido = {
            "nome": "Sem Disciplina"
        }
        response = self.app.post('/professor', json=professor_invalido)
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_update_professor_existente(self):
        update_data = {"nome": "Ana Modificada", "disciplina": "Física"}
        response = self.app.put('/professor/1', json=update_data)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["message"], "professor atualizado com sucesso")
        self.assertEqual(professores[0]["disciplina"], "Física")

    def test_update_professor_inexistente(self):
        update_data = {"nome": "Nome Inválido", "disciplina": "Química"}
        response = self.app.put('/professor/999', json=update_data)
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)
        self.assertEqual(data["error"], "professor nao encontrado")

    def test_delete_professor_existente(self):
        response = self.app.delete('/professor/2')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["message"], "professor removido com sucesso")

    def test_delete_professor_inexistente(self):
        response = self.app.delete('/professor/999')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)
        self.assertEqual(data["error"], "professor nao encontrado")

    def test_get_turma_existente(self):
        response = self.app.get('/turma/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["turma"]["nome"], "Turma A")

    def test_get_turma_inexistente(self):
        response = self.app.get('/turma/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "turma nao encontrada")

    def test_create_turma(self):
        nova_turma = {
            "nome": "Turma C",
            "id_professor": 1,
        }
        response = self.app.post('/turma', json=nova_turma)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["message"], "turma criada com sucesso")


    def test_create_turma_dados_invalidos(self):
        turma_invalida = {
            "nome": "Turma Sem Professor"
        }
        response = self.app.post('/turma', json=turma_invalida)
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_update_turma_existente(self):
        update_data = {"nome": "Turma X", "id_professor": 1}
        response = self.app.put('/turma/1', json=update_data)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["message"], "turma atualizada com sucesso")
        self.assertEqual(turmas[0]["id_professor"], 1)

    def test_update_turma_existente_professor_inexistente(self):
        update_data = {"nome": "Turma X", "id_professor": 6}
        response = self.app.put('/turma/1', json=update_data)
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)
        self.assertEqual(data["error"], "professor 6 nao encontrado")

    def test_update_turma_inexistente(self):
        update_data = {"nome": "Turma Z", "professor": "Inexistente"}
        response = self.app.put('/turma/999', json=update_data)
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)
        self.assertEqual(data["error"], "turma nao encontrada")

    def test_delete_turma_existente(self):
        response = self.app.delete('/turma/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["message"], "turma removida com sucesso")

    def test_delete_turma_inexistente(self):
        response = self.app.delete('/turma/999')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)
        self.assertEqual(data["error"], "turma nao encontrada")

if __name__ == '__main__':
    unittest.main()
