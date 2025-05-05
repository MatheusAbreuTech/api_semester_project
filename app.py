from flask import Flask
from database.db import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    

    with app.app_context():
        from swagger.config_swagger import configure_swagger
        configure_swagger(app)
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)