from config import app
from routes.alunos_routes import alunos_blueprint
from routes.professores_routes import professores_blueprint
from routes.turmas_routes import turmas_blueprint

app.register_blueprint(professores_blueprint)
app.register_blueprint(alunos_blueprint)
app.register_blueprint(turmas_blueprint)

if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )
