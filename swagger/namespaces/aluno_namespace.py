from flask_restx import Namespace, Resource

alunos_ns = Namespace("Alunos", description="Operações relacionadas a alunos")

@alunos_ns.route("/")
class AlunoList(Resource):
    def get(self):
        return {"message": "Lista de alunos"}

    def post(self):
        return {"message": "Aluno criado"}, 201

@alunos_ns.route("/<int:aluno_id>")
class Aluno(Resource):
    def get(self, aluno_id):
        return {"message": f"Aluno {aluno_id}"}

    def put(self, aluno_id):
        return {"message": f"Aluno {aluno_id} atualizado"}, 200

    def delete(self, aluno_id):
        return {"message": f"Aluno {aluno_id} deletado"}, 200
