from flask import (Blueprint, request)
from turma.turma_model import TurmaModel

turmas_blueprint = Blueprint('turmas', __name__)
turmas_model = TurmaModel()

@turmas_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    return turmas_model.get_turmas()

@turmas_blueprint.route("/turmas/<int:turma_id>", methods=['GET'])
def get_turma(turma_id):
    return turmas_model.get_turma(turma_id)

@turmas_blueprint.route("/turmas", methods=['POST'])
def create_turma():
    data = request.json
    return turmas_model.create_turma(data)

@turmas_blueprint.route("/turmas/<int:turma_id>", methods=['PUT'])
def update_turma(turma_id):
    data = request.json
    return turmas_model.update_turma(turma_id, data)

@turmas_blueprint.route("/turmas/<int:turma_id>", methods=['DELETE'])
def delete_turma(turma_id):
    return turmas_model.delete_turma(turma_id)

@turmas_blueprint.route('/turmas/<int:turma_id>/professor/<int:professor_id>', methods=['POST'])
def add_professor(turma_id, professor_id):
    return turmas_model.add_professor(turma_id, professor_id)

@turmas_blueprint.route('/turmas/<int:turma_id>/professor', methods=['DELETE'])
def remove_professor(turma_id):
    return turmas_model.remove_professor(turma_id)

@turmas_blueprint.route('/turmas/<inueprint.routet:turma_id>/alunos/<int:aluno_id>', methods=['POST'])
def add_student(turma_id, aluno_id):
    return turmas_model.add_student(turma_id, aluno_id)

