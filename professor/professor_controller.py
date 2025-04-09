from config import app
from flask import Blueprint,request
from professor import professor_model
from professor.professor_model import ProfessorModel

professores_blueprint = Blueprint('professor', __name__)
professores_model = ProfessorModel()

@app.route('/professores', methods=['GET'])
def get_professores():
  return professores_model.get_professores()

@app.route('/professor/<int:professor_id>', methods=['GET'])
def get_professor(professor_id):
  return professores_model.get_professor(professor_id)

@app.route('/professor', methods=['POST'])
def create_professor():
  data = request.json
  return professores_model.create_professor(data)


@app.route('/professor/<int:professor_id>', methods=['PUT'])
def update_professor(professor_id):
  data = request.json
  return professores_model.update_professor(professor_id,data)


@app.route('/professor/<int:professor_id>', methods=['DELETE'])
def delete_professor(professor_id):
  return professores_model.delete_professor(professor_id)