from flask import Blueprint, jsonify, request

alunos_blueprint = Blueprint('alunos', __name__)

alunos =  [
        {"id": 1, "nome": "João Pereira", "idade": 15, "turma_id": 101},
        {"id": 2, "nome": "Mariana Lima", "idade": 14, "turma_id": 101},
        {"id": 3, "nome": "Lucas Oliveira", "idade": 16, "turma_id": 102},
        {"id": 4, "nome": "Beatriz Santos", "idade": 15, "turma_id": 103},
        {"id": 5, "nome": "Gabriel Martins", "idade": 14, "turma_id": 103}
    ]

@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(alunos)

@alunos_blueprint.route('/alunos/<int:id>', methods=['GET'])
def get_aluno(id):
    aluno = next((a for a in alunos if a ['id'] == id), None)
    if aluno:
        return jsonify(aluno)
    return jsonify({"erro": "Aluno não existe."}), 404

@alunos_blueprint.route('/alunos', methods=['POST'])
def add_aluno():
    novo_aluno = request.json
    novo_aluno["id"] = alunos[-1]["id"] + 1 if alunos else 1
    alunos.append(novo_aluno)
    return jsonify(novo_aluno), 201

@alunos_blueprint.route('/alunos/<int:id>', methods=['PUT'])
def update_aluno(id):
    aluno = next((a for a in alunos if a['id'] == id), None)
    if aluno:
        data = request.json
        aluno.update(data)
        return jsonify(aluno)
    return jsonify({"erro": "Aluno não foi encontrado."}), 404

@alunos_blueprint.route('/alunos/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    global alunos
    alunos = [a for a in alunos if a['id'] != id]
    return jsonify({"mensagem": "Aluno removido."})
