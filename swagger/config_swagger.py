from . import api
from aluno.aluno_controller import alunos_ns

def configure_swagger(app):
    api.init_app(app)
    api.add_namespace(alunos_ns, path="/alunos")
