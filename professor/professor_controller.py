from flask import Blueprint,request
from professor import professor_model
from flask_restx import Namespace, Resource, fields
from professor.professor_service import ProfessorService

professores_service = ProfessorService()

professores_ns = Namespace('professores', description='Operações relacionadas aos professores')

professor_input = professores_ns.model('ProfessorInput', {
    'nome': fields.String(required=True, description='Nome do professor', min_length=3),
    'idade': fields.Integer(required=True, description='Idade do professor', min=1),
    'turma_id': fields.Integer(required=False, description='ID da turma')
})

professor_output = professores_ns.model('ProfessorOutput', {
    'id': fields.Integer(required=True, description='ID do professor'),
    'nome': fields.String(required=True, description='Nome do professor'),
    'idade': fields.Integer(required=True, description='Idade do professor'),
    'turma_id': fields.Integer(required=False, description='ID da turma')
})

professor_service = ProfessorService()

@professores_ns.route('/', strict_slashes=False)
class ProfessorListResource(Resource):
    @professores_ns.doc('list_professores')
    @professores_ns.marshal_list_with(professor_output)
    def get(self):
        professores, status_code = professor_service.get_professores()
        return professores, status_code

    @professores_ns.doc('create_professor')
    @professores_ns.expect(professor_input)
    @professores_ns.marshal_with(professor_output, code=201)
    @professores_ns.response(400, 'Erro ao criar professor')
    @professores_ns.response(500, 'Erro interno do servidor')
    def post(self):
        data = request.get_json()
        response, status_code = professor_service.create_professor(data)
        return response, status_code

@professores_ns.route('/<int:professor_id>', strict_slashes=False)
class ProfessorResource(Resource):
    @professores_ns.doc('get_professor')
    @professores_ns.marshal_with(professor_output)
    @professores_ns.response(404, 'Nenhum professor encontrado')
    @professores_ns.param('professor_id', 'O ID do professor')
    def get(self, professor_id):
        professor, status_code = professor_service.get_professor(professor_id)
        return professor, status_code
    
    @professores_ns.doc('update_professor')
    @professores_ns.marshal_with(professor_output)
    @professores_ns.response(400, 'Dados inválidos')
    @professores_ns.response(404, 'Nenhum professor encontrado')
    @professores_ns.response(500, 'Erro interno do servidor')
    @professores_ns.param('professor_id', 'O ID do professor')
    @professores_ns.expect(professor_input)
    def put(self, professor_id):
        data = request.get_json()
        response, status_code = professor_service.update_professor(professor_id, data)
        return response, status_code

    @professores_ns.doc('delete_professor')
    @professores_ns.response(204, 'Professor deletado com sucesso')
    @professores_ns.response(404, 'Nenhum professor encontrado')
    @professores_ns.response(500, 'Erro interno do servidor')
    @professores_ns.param('professor_id', 'O ID do professor')
    def delete(self, professor_id):
        response, status_code = professor_service.delete_professor(professor_id)
        return response, status_code
