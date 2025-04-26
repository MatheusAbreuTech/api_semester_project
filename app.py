from flask import  jsonify, request
from config import app

from turma.turma_controller import turmas_blueprint
from professor.professor_controller import professores_blueprint
from swagger.config_swagger import configure_swagger

app.register_blueprint(turmas_blueprint)
app.register_blueprint(professores_blueprint)

configure_swagger(app)

if __name__ == '__main__':
  app.run(host=app.config["HOST"],debug=app.config['DEBUG'] )