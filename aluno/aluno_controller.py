from flask import Blueprint
from aluno.aluno_model import AlunoModel

alunos_blueprint = Blueprint('alunos', __name__)
alunos_model = AlunoModel()

@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    return alunos_model.get_alunos()

@alunos_blueprint.route('/alunos/<int:aluno_id>', methods=['GET'])
def get_aluno(aluno_id):
    return alunos_model.get_aluno(aluno_id)

@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.json
    return alunos_model.create_aluno(data)

@alunos_blueprint.route('/alunos/<int:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    data = request.json
    return alunos_model.update_aluno(aluno_id, data)

@alunos_blueprint.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    return alunos_model.delete_aluno(aluno_id)