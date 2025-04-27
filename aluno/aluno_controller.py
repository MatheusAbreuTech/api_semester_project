from flask import request
from flask_restx import Namespace, Resource, fields
from aluno.aluno_service import AlunoService

alunos_ns = Namespace('alunos', description='Operações relacionadas aos alunos')

aluno_input = alunos_ns.model('AlunoInput', {
    'nome': fields.String(required=True, description='Nome do aluno', min_length=3),
    'idade': fields.Integer(required=True, description='Idade do aluno', min=1),
    'turma_id': fields.Integer(required=False, description='ID da turma')
})

aluno_output = alunos_ns.model('AlunoOutput', {
    'id': fields.Integer(required=True, description='ID do aluno'),
    'nome': fields.String(required=True, description='Nome do aluno'),
    'idade': fields.Integer(required=True, description='Idade do aluno'),
    'turma_id': fields.Integer(required=False, description='ID da turma')
})

aluno_service = AlunoService()

@alunos_ns.route('/', strict_slashes=False)
class AlunoListResource(Resource):
    @alunos_ns.doc('list_alunos')
    @alunos_ns.marshal_list_with(aluno_output)
    def get(self):
        alunos, status_code = aluno_service.get_alunos()
        return alunos, status_code

    @alunos_ns.doc('create_aluno')
    @alunos_ns.expect(aluno_input)
    @alunos_ns.marshal_with(aluno_output, code=201)
    @alunos_ns.response(400, 'Erro ao criar aluno')
    @alunos_ns.response(500, 'Erro interno do servidor')
    def post(self):
        data = request.get_json()
        response, status_code = aluno_service.create_aluno(data)
        return response, status_code

@alunos_ns.route('/<int:aluno_id>', strict_slashes=False)
class AlunoResource(Resource):
    @alunos_ns.doc('get_aluno')
    @alunos_ns.marshal_with(aluno_output)
    @alunos_ns.response(404, 'Nenhum aluno encontrado')
    @alunos_ns.param('aluno_id', 'O ID do aluno')
    def get(self, aluno_id):
        aluno, status_code = aluno_service.get_aluno(aluno_id)
        return aluno, status_code
    
    @alunos_ns.doc('update_aluno')
    @alunos_ns.marshal_with(aluno_output)
    @alunos_ns.response(400, 'Dados inválidos')
    @alunos_ns.response(404, 'Nenhum aluno encontrado')
    @alunos_ns.response(500, 'Erro interno do servidor')
    @alunos_ns.param('aluno_id', 'O ID do aluno')
    @alunos_ns.expect(aluno_input)
    def put(self, aluno_id):
        data = request.get_json()
        response, status_code = aluno_service.update_aluno(aluno_id, data)
        return response, status_code

    @alunos_ns.doc('delete_aluno')
    @alunos_ns.response(204, 'Aluno deletado com sucesso')
    @alunos_ns.response(404, 'Nenhum aluno encontrado')
    @alunos_ns.response(500, 'Erro interno do servidor')
    @alunos_ns.param('aluno_id', 'O ID do aluno')
    def delete(self, aluno_id):
        response, status_code = aluno_service.delete_aluno(aluno_id)
        return response, status_code
