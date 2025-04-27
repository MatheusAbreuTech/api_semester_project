from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from swagger.config_swagger import configure_swagger
from turma.turma_controller import turmas_blueprint
from professor.professor_controller import professores_blueprint

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)

    app.register_blueprint(turmas_blueprint)
    app.register_blueprint(professores_blueprint)

    configure_swagger(app)

    return app

app = create_app()
with app.app_context():
    db.create_all()
