from flask import Flask, jsonify, request

app = Flask(__name__)

alunos =  [
        {"id": 1, "nome": "João Pereira", "idade": 15},
        {"id": 2, "nome": "Mariana Lima", "idade": 14},
        {"id": 3, "nome": "Lucas Oliveira", "idade": 16},
        {"id": 4, "nome": "Beatriz Santos", "idade": 15},
        {"id": 5, "nome": "Gabriel Martins", "idade": 14}
]

def valid_data_student(data):
    required_fields = ["nome", "idade", "turma_id"]
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"O campo {field} é obrigatório."
    if not isinstance(data["idade"], int) or data["idade"] <= 0:
        return False, "O campo 'idade' deve ser um número inteiro positivo."
    return True, ""

@app.route('/alunos', methods=['GET'])
def get_alunos():
    data = alunos

    if data is None:
        return jsonify([])
    return jsonify(alunos)

@app.route('/alunos/<int:aluno_id>', methods=['GET'])
def get_aluno(aluno_id):
    for aluno in alunos:
        if aluno['id'] == aluno_id:
            return jsonify({
                "aluno": aluno,
            })

    return jsonify({"erro": "Aluno não existe."}), 404

@app.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.json

    valid, message = valid_data_student(data)
    if not valid:
        return jsonify({"erro": message}), 400

    aluno = {
        "id": len(alunos) + 1,
        "nome": data["nome"],
        "idade": data["idade"],
        "turma_id": data["turma_id"]
    }

    alunos.append(aluno)

    return jsonify({
        "message": "Aluno criada com sucesso!",
        "alunos": alunos
    })

@app.route('/alunos/<int:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    for aluno in alunos:
        if aluno['id'] == aluno_id:
            data = request.json

            valid, message = valid_data_student(data)
            if not valid:
                return jsonify({"erro": message}), 400

            aluno.update(data)

            return jsonify({
                "message": "Aluno atualizado com sucesso!",
                "alunos": alunos
            })

    return jsonify({"error": "aluno não encontrado"})



@app.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    for aluno in alunos:
        if aluno['id'] == aluno_id:
            alunos.remove(aluno)
            return jsonify({"message": "Aluno deletado com sucesso!"})
    return jsonify({"error": "aluno não encontrado"}), 404


if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )
