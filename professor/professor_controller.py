from flask import request
from flask_restx import Namespace, Resource, fields
from professor.professor_service import ProfessorService

professores_ns = Namespace('professores', description='Operações relacionadas aos professores')
professor_service = ProfessorService()

professor_input = professores_ns.model('ProfessorInput', {
    'nome': fields.String(required=True, description='Nome do professor', min_length=3),
    'id_disciplina': fields.Integer(required=True, description='Matéria que o professor leciona'),
    'idade':fields.Integer(required=True, description='idade'),
    'observacoes':fields.String(required=False, description='observações sobre o professor')
})

professor_output = professores_ns.model('ProfessorOutput', {
    'id': fields.Integer(required=True, description='ID do professor'),
    'nome': fields.String(required=True, description='Nome do professor'),
    'materia': fields.String(required=True, description='Matéria que o professor leciona'),
    'id_disciplina': fields.String(required=True, description='ID da matéria que o professor leciona'),
    'idade':fields.Integer(required=True, description='idade')
})

@professores_ns.route('/')
class ProfessorListResource(Resource):
    @professores_ns.doc('list_professores')
    @professores_ns.marshal_list_with(professor_output)
    def get(self):
        response, status_code = professor_service.get_professores()
        return response, status_code

    @professores_ns.doc('create_professor')
    @professores_ns.expect(professor_input)
    @professores_ns.response(201, 'Success', professor_output)
    @professores_ns.response(400, 'Validation Error')
    @professores_ns.response(500, 'Internal Error')
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"erro": "Dados não fornecidos"}, 400
            
            response, status_code = professor_service.create_professor(data)
            
            return response, status_code
                
        except Exception as e:
            return {"erro": f"Erro interno no servidor: {str(e)}"}, 500

@professores_ns.route('/<int:professor_id>', strict_slashes=False)
class ProfessorResource(Resource):
    @professores_ns.doc('get_professor')
    @professores_ns.marshal_with(professor_output)
    @professores_ns.response(404, 'Nenhum professor encontrado')
    @professores_ns.response(500, 'Erro interno do servidor')
    def get(self, professor_id):
        response, status_code = professor_service.get_professor(professor_id)
        return response, status_code
    
    @professores_ns.doc('update_professor')
    @professores_ns.expect(professor_input)
    @professores_ns.response(400, 'Dados inválidos')
    @professores_ns.response(200, 'Success', professor_output)
    @professores_ns.response(404, 'Nenhum professor encontrado')
    @professores_ns.response(500, 'Erro interno do servidor')
    def put(self, professor_id):
        data = request.json
        response, status_code = professor_service.update_professor(professor_id, data)
        return response, status_code

    @professores_ns.doc('delete_professor')
    @professores_ns.response(204, 'Professor deletado com sucesso')
    @professores_ns.response(404, 'Nenhum professor encontrado')
    @professores_ns.response(500, 'Erro interno do servidor')
    def delete(self, professor_id):
        response, status_code = professor_service.delete_professor(professor_id)
        return response, status_code