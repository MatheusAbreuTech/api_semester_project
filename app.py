from flask import Flask
from turma.turma_controller import turmas_blueprint
from professor.professor_controller import professores_blueprint
from database.db import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    app.register_blueprint(turmas_blueprint)
    app.register_blueprint(professores_blueprint)

    with app.app_context():
        from swagger.config_swagger import configure_swagger
        configure_swagger(app)
        db.create_all()

    return app

app = create_app()