from flask import  jsonify, request
from config import app
from aluno.aluno_controller import alunos_blueprint
from database.alunos import alunos
from database.professores import professores
from database.turmas import turmas
from turma.turma_controller import turmas_blueprint
from professor.professor_controller import professores_blueprint

app.register_blueprint(alunos_blueprint)
app.register_blueprint(turmas_blueprint)
app.register_blueprint(professores_blueprint)

if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )