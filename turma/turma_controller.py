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