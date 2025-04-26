from flask_restx import Namespace, Resource, fields
from flask import request
from turma.turma_model import TurmaModel

turmas_ns = Namespace('turmas', description='Operações relacionadas às turmas')

# Instancia do Model
turmas_model = TurmaModel()

# Modelo de exemplo para documentação Swagger (Request Body)
turma_input = turmas_ns.model('TurmaInput', {
    'nome': fields.String(required=True, description='Nome da turma'),
    'descricao': fields.String(required=False, description='Descrição da turma')
})

# Rotas

@turmas_ns.route('')
class TurmasList(Resource):
    @turmas_ns.doc('list_turmas')
    def get(self):
        """Lista todas as turmas"""
        return turmas_model.get_turmas()

    @turmas_ns.expect(turma_input)
    @turmas_ns.doc('create_turma')
    def post(self):
        """Cria uma nova turma"""
        data = request.json
        return turmas_model.create_turma(data)


@turmas_ns.route('/<int:turma_id>')
@turmas_ns.param('turma_id', 'O ID da turma')
class TurmaResource(Resource):
    @turmas_ns.doc('get_turma')
    def get(self, turma_id):
        """Busca uma turma pelo ID"""
        return turmas_model.get_turma(turma_id)

    @turmas_ns.expect(turma_input)
    @turmas_ns.doc('update_turma')
    def put(self, turma_id):
        """Atualiza uma turma existente"""
        data = request.json
        return turmas_model.update_turma(turma_id, data)

    @turmas_ns.doc('delete_turma')
    def delete(self, turma_id):
        """Deleta uma turma pelo ID"""
        return turmas_model.delete_turma(turma_id)


@turmas_ns.route('/<int:turma_id>/professor/<int:professor_id>')
@turmas_ns.param('turma_id', 'O ID da turma')
@turmas_ns.param('professor_id', 'O ID do professor')
class TurmaProfessorResource(Resource):
    @turmas_ns.doc('add_professor')
    def post(self, turma_id, professor_id):
        """Adiciona um professor a uma turma"""
        return turmas_model.add_professor(turma_id, professor_id)


@turmas_ns.route('/<int:turma_id>/professor')
@turmas_ns.param('turma_id', 'O ID da turma')
class TurmaRemoveProfessorResource(Resource):
    @turmas_ns.doc('remove_professor')
    def delete(self, turma_id):
        """Remove o professor de uma turma"""
        return turmas_model.remove_professor(turma_id)


@turmas_ns.route('/<int:turma_id>/alunos/<int:aluno_id>')
@turmas_ns.param('turma_id', 'O ID da turma')
@turmas_ns.param('aluno_id', 'O ID do aluno')
class TurmaAlunoResource(Resource):
    @turmas_ns.doc('add_student')
    def post(self, turma_id, aluno_id):
        """Adiciona um aluno a uma turma"""
        return turmas_model.add_student(turma_id, aluno_id)


@turmas_ns.route('/<int:turma_id>/aluno/<int:aluno_id>')
@turmas_ns.param('turma_id', 'O ID da turma')
@turmas_ns.param('aluno_id', 'O ID do aluno')
class TurmaRemoveAlunoResource(Resource):
    @turmas_ns.doc('remove_student')
    def delete(self, turma_id, aluno_id):
        """Remove um aluno de uma turma"""
        return turmas_model.remove_student(turma_id, aluno_id)
