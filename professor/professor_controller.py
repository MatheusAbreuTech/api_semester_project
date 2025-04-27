from flask import Blueprint,request
from professor import professor_model
from professor.professor_model import ProfessorModel

professores_blueprint = Blueprint('professor', __name__)
professores_model = ProfessorModel()

@professores_blueprint.route('/professores', methods=['GET'])
def get_professores():
  return professores_model.get_professores()

@professores_blueprint.route('/professor/<int:professor_id>', methods=['GET'])
def get_professor(professor_id):
  return professores_model.get_professor(professor_id)

@professores_blueprint.route('/professor', methods=['POST'])
def create_professor():
  data = request.json
  return professores_model.create_professor(data)


@professores_blueprint.route('/professor/<int:professor_id>', methods=['PUT'])
def update_professor(professor_id):
  data = request.json
  return professores_model.update_professor(professor_id,data)


@professores_blueprint.route('/professor/<int:professor_id>', methods=['DELETE'])
def delete_professor(professor_id):
  return professores_model.delete_professor(professor_id)