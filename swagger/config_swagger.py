from flask_restx import Api

api = Api(version='1.0', title='API Escola', description='API para gestão escolar')

def configure_swagger(app):
    from aluno.aluno_controller import alunos_ns
    from professor.professor_controller import professores_ns
    api.init_app(app)
    api.add_namespace(alunos_ns, path="/alunos")
    api.add_namespace(professores_ns, path="/professores")
