from flask import request
from flask_restx import Namespace, Resource, fields
from aluno.aluno_service import AlunoService
from datetime import date

alunos_ns = Namespace('alunos', description='Operações relacionadas aos alunos')

aluno_input = alunos_ns.model('AlunoInput', {
    'nome': fields.String(required=True, description='Nome do aluno', min_length=3),
    'data_nasc': fields.String(required=True, description='Data de nascimento no formato YYYY-MM-DD', example='2000-01-01'),
    'nota_semestre1': fields.Float(required=True, description='Nota Primeiro semestre'),
    'nota_semestre2': fields.Float(required=False, description='Nota Segundo semestre')
})

aluno_output = alunos_ns.model('AlunoOutput', {
    'id': fields.Integer(required=True, description='ID do aluno'),
    'nome': fields.String(required=True, description='Nome do aluno'),
    'idade': fields.Integer(required=True, description='Idade do aluno'),
    'data_nasc': fields.String(required=True, description='Data de nascimento no formato YYYY-MM-DD', example='2000-01-01'),
    'turma_id': fields.Integer(required=False, description='ID da turma'),
    'nota_semestre1': fields.Float(required=True, description='Nota Primeiro semestre'),
    'nota_semestre2': fields.Float(required=True, description='Nota Segundo semestre'),
    'media_final': fields.Float(required=False, description='Media final')
})

aluno_service = AlunoService()

@alunos_ns.route('/')
class AlunoListResource(Resource):
    @alunos_ns.doc('list_alunos')
    @alunos_ns.marshal_list_with(aluno_output)
    def get(self):
        response, status_code = aluno_service.get_alunos()
        return response, status_code

    @alunos_ns.doc('create_aluno')
    @alunos_ns.expect(aluno_input)
    @alunos_ns.response(201, 'Success', aluno_output)
    @alunos_ns.response(400, 'Validation Error')
    @alunos_ns.response(500, 'Internal Error')
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"erro": "Dados não fornecidos"}, 400
                
            response, status_code = aluno_service.create_aluno(data)
            return response, status_code
            
        except Exception as e:
            return {"erro": f"Erro no controller: {str(e)}"}, 500

@alunos_ns.route('/<int:aluno_id>')
class AlunoResource(Resource):
    @alunos_ns.doc('get_aluno')
    @alunos_ns.marshal_with(aluno_output)
    @alunos_ns.response(404, 'Aluno não encontrado')
    def get(self, aluno_id):
        response, status_code = aluno_service.get_aluno(aluno_id)
        return response, status_code
    
    @alunos_ns.doc('update_aluno')
    @alunos_ns.expect(aluno_input)
    @alunos_ns.marshal_with(aluno_output)
    @alunos_ns.response(400, 'Dados inválidos')
    @alunos_ns.response(404, 'Aluno não encontrado')
    def put(self, aluno_id):
        data = request.get_json()
        response, status_code = aluno_service.update_aluno(aluno_id, data)
        return response, status_code

    @alunos_ns.doc('delete_aluno')
    @alunos_ns.response(204, 'Aluno deletado')
    @alunos_ns.response(404, 'Aluno não encontrado')
    def delete(self, aluno_id):
        response, status_code = aluno_service.delete_aluno(aluno_id)
        return response, status_code