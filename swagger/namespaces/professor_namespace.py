# arquivo: swagger/namespaces/professor_namespace.py

from flask_restx import Namespace, Resource, fields
from flask import request
from professor.professor_model import ProfessorModel

professores_ns = Namespace('professores', description='Operações relacionadas aos professores')

# Instancia do Model
professor_model = ProfessorModel()

# Modelo de entrada para criar/atualizar professor
professor_input = professores_ns.model('ProfessorInput', {
    'nome': fields.String(required=True, description='Nome do professor'),
    'disciplina': fields.String(required=True, description='Disciplina que o professor leciona')
})

# Rotas

@professores_ns.route('')
class ProfessoresList(Resource):
    @professores_ns.doc('list_professores')
    def get(self):
        """Lista todos os professores"""
        return professor_model.get_professores()

    @professores_ns.expect(professor_input)
    @professores_ns.doc('create_professor')
    def post(self):
        """Cria um novo professor"""
        data = request.json
        return professor_model.create_professor(data)


@professores_ns.route('/<int:professor_id>')
@professores_ns.param('professor_id', 'O ID do professor')
class ProfessorResource(Resource):
    @professores_ns.doc('get_professor')
    def get(self, professor_id):
        """Busca um professor pelo ID"""
        return professor_model.get_professor(professor_id)

    @professores_ns.expect(professor_input)
    @professores_ns.doc('update_professor')
    def put(self, professor_id):
        """Atualiza um professor existente"""
        data = request.json
        return professor_model.update_professor(professor_id, data)

    @professores_ns.doc('delete_professor')
    def delete(self, professor_id):
        """Deleta um professor pelo ID"""
        return professor_model.delete_professor(professor_id)
