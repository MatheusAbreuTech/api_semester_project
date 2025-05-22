from flask import  request
from turma.turma_service import TurmaService
from flask_restx import Namespace, Resource, fields
from turma.turma_service import TurmaService


turmas_service = TurmaService()
turmas_ns = Namespace('turmas', description='Operações relacionadas às turmas')

turma_input = turmas_ns.model('TurmaInput', {
    'descricao': fields.String(required=True, description='Descricao da turma'),
    'ativo':fields.Boolean(required=True, description='Disponibilidade da turma')
    
})

turma_output = turmas_ns.model('TurmaOutput', {
    'id': fields.Integer(required=True, description='Id da turma'),
    "professor_id": fields.Integer(required=False, description='Id do professor'),
    "ativo":fields.Boolean(required=True, description='Disponibilidade da turma'),
    'descricao': fields.String(required=True, description='Descricao da turma'),

})

turmas_service= TurmaService()

@turmas_ns.route('/turmas', strict_slashes=False)
class TurmasList(Resource):
    @turmas_ns.doc('list_turmas')
    @turmas_ns.marshal_list_with(turma_output)
    def get(self):
        turmas, status_code = turmas_service.get_turmas()
        return turmas, status_code

    @turmas_ns.doc('create_turma')
    @turmas_ns.expect(turma_input)
    @turmas_ns.response(201, 'Success', turma_output)
    @turmas_ns.response(400, 'Erro ao criar tur ma')
    @turmas_ns.response(500, 'Erro interno do servidor')
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"erro": "Dados não fornecidos"}, 400

            response, status_code = turmas_service.create_turma(data)
            return response, status_code

        except Exception as e:
            return {"erro": f"Erro interno no servidor: {str(e)}"}, 500

@turmas_ns.route('/turmas/<int:turma_id>', strict_slashes=False)
class TurmaResource(Resource):
    @turmas_ns.doc('get_turma')
    @turmas_ns.response(200, 'Success', turma_output)
    @turmas_ns.response(404, 'Nenhuma turma encontrada')
    def get(self, turma_id):
        turma, status_code = turmas_service.get_turma(turma_id)
        return turma, status_code

    @turmas_ns.doc('update_turma')
    @turmas_ns.expect(turma_input)
    @turmas_ns.response(200, 'Success', turma_output)
    @turmas_ns.response(400, 'Dados inválidos')
    @turmas_ns.response(404, 'Nenhuma turma encontrada')
    @turmas_ns.response(500, 'Erro interno do servidor')
    def put(self, turma_id):
        data = request.json
        response, status_code = turmas_service.update_turma(turma_id, data)
        return response, status_code

    @turmas_ns.doc('delete_turma')
    @turmas_ns.response(204, 'Turma deletada com sucesso')
    @turmas_ns.response(404, 'Nenhuma turma encontrada')
    def delete(self, turma_id):
        response, status_code = turmas_service.delete_turma(turma_id)
        return response, status_code

@turmas_ns.route('/<int:turma_id>/professor/<int:professor_id>', strict_slashes=False)
class TurmaProfessorResource(Resource):
    @turmas_ns.doc('add_professor')
    @turmas_ns.response(200, 'Professor adicionado com sucesso')
    @turmas_ns.response(404, 'professor nao encontrado')
    @turmas_ns.response(404, 'turma nao encontrada')
    def post(self, turma_id, professor_id):
        response, status_code = turmas_service.add_professor(turma_id, professor_id)
        return response, status_code

    @turmas_ns.doc('remove_professor')
    @turmas_ns.response(200, 'Professor removido com sucesso')
    @turmas_ns.response(404, 'professor nao encontrado')
    @turmas_ns.response(404, 'turma nao encontrada')
    def delete(self, turma_id, professor_id):
        response, status_code = turmas_service.remove_professor(turma_id, professor_id)
        return response, status_code

@turmas_ns.route('/<int:turma_id>/alunos/<int:aluno_id>', strict_slashes=False)
class TurmaAlunoResource(Resource):
    @turmas_ns.doc('add_student')
    @turmas_ns.response(200, 'Aluno adicionado com sucesso')
    @turmas_ns.response(404, 'Nenhuma turma ou aluno encontrado')
    def post(self, turma_id, aluno_id):
        response, status_code = turmas_service.add_student(turma_id, aluno_id)
        return response, status_code

    @turmas_ns.doc('remove_student')
    @turmas_ns.response(200, 'Aluno removido com sucesso')
    @turmas_ns.response(404, 'Nenhuma turma ou aluno encontrado')
    def delete(self, turma_id, aluno_id):
        response, status_code = turmas_service.remove_student(turma_id, aluno_id)
        return response, status_code


