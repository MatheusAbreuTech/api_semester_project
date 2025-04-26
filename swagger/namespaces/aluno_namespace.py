# # arquivo: swagger/namespaces/aluno_namespace.py

# from flask_restx import Namespace, Resource, fields
# from flask import request
# from aluno.aluno_model import AlunoModel

# alunos_ns = Namespace('alunos', description='Operações relacionadas aos alunos')

# # Instância do Model
# aluno_model = AlunoModel()

# # Modelo de entrada para criar/atualizar aluno
# aluno_input = alunos_ns.model('AlunoInput', {
#     'nome': fields.String(required=True, description='Nome do aluno'),
#     'idade': fields.Integer(required=True, description='Idade do aluno')
# })

# # Rotas

# @alunos_ns.route('')
# class AlunosList(Resource):
#     @alunos_ns.doc('list_alunos')
#     def get(self):
#         """Lista todos os alunos"""
#         return aluno_model.get_alunos()

#     @alunos_ns.expect(aluno_input)
#     @alunos_ns.doc('create_aluno')
#     def post(self):
#         """Cria um novo aluno"""
#         data = request.json
#         return aluno_model.create_aluno(data)


# @alunos_ns.route('/<int:aluno_id>')
# @alunos_ns.param('aluno_id', 'O ID do aluno')
# class AlunoResource(Resource):
#     @alunos_ns.doc('get_aluno')
#     def get(self, aluno_id):
#         """Busca um aluno pelo ID"""
#         return aluno_model.get_aluno(aluno_id)

#     @alunos_ns.expect(aluno_input)
#     @alunos_ns.doc('update_aluno')
#     def put(self, aluno_id):
#         """Atualiza um aluno existente"""
#         data = request.json
#         return aluno_model.update_aluno(aluno_id, data)

#     @alunos_ns.doc('delete_aluno')
#     def delete(self, aluno_id):
#         """Deleta um aluno pelo ID"""
#         return aluno_model.delete_aluno(aluno_id)
