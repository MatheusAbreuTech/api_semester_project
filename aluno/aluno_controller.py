from flask import request
from flask_restx import Namespace, Resource, fields
from aluno.aluno_model import AlunoModel

alunos_model = AlunoModel()

alunos_ns = Namespace('alunos', description='Operações relacionadas aos alunos')

aluno_input = alunos_ns.model('AlunoInput', {
    'nome': fields.String(required=True, description='Nome do aluno'),
    'idade': fields.Integer(required=True, description='Idade do aluno')
})

@alunos_ns.route('/')
class AlunoListResource(Resource):
    @alunos_ns.doc('list_alunos')
    def get(self):
        return alunos_model.get_alunos()

    @alunos_ns.doc('create_aluno')
    @alunos_ns.expect(aluno_input)
    def post(self):
        data = request.json
        return alunos_model.create_aluno(data)

@alunos_ns.route('/<int:aluno_id>')
class AlunoResource(Resource):
    @alunos_ns.doc('get_aluno')
    @alunos_ns.param('aluno_id', 'O ID do aluno')
    def get(self, aluno_id):
        return alunos_model.get_aluno(aluno_id)

    @alunos_ns.doc('update_aluno')
    @alunos_ns.param('aluno_id', 'O ID do aluno')
    @alunos_ns.expect(aluno_input)
    def put(self, aluno_id):
        data = request.json
        return alunos_model.update_aluno(aluno_id, data)

    @alunos_ns.doc('delete_aluno')
    @alunos_ns.param('aluno_id', 'O ID do aluno')
    def delete(self, aluno_id):
        return alunos_model.delete_aluno(aluno_id)
