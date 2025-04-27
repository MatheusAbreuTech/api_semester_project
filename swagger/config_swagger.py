from . import api

def configure_swagger(app):
    from aluno.aluno_controller import alunos_ns
    api.init_app(app)
    api.add_namespace(alunos_ns, path="/alunos")
