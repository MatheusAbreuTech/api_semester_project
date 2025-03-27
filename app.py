from flask import Flask, jsonify, request
from aluno.aluno_model import AlunoModel
app = Flask(__name__)

alunos =  [
        {"id": 1, "nome": "João Pereira", "idade": 15, "turma_id": 1},
        {"id": 2, "nome": "Mariana Lima", "idade": 14, "turma_id": 1},
        {"id": 3, "nome": "Lucas Oliveira", "idade": 16, "turma_id": 2},
        {"id": 4, "nome": "Beatriz Santos", "idade": 15, "turma_id": 2},
        {"id": 5, "nome": "Gabriel Martins", "idade": 14, "turma_id": 2}
]

professores = [
    {"id": 1, "nome": "Ana Silva", "disciplina": "Matemática"},
    {"id": 2, "nome": "Carlos Souza", "disciplina": "História"},
    {"id": 3, "nome": "Fernanda Costa", "disciplina": "Biologia"}
]

turmas = [
    {"id": 1, "nome": "Turma A", "professor": "Ana Silva", },
    {"id": 2, "nome": "Turma B", "professor": "Carlos Souza", },
    {"id": 3, "nome": "Turma C", "professor": "Fernanda Costa", }
]

alunos_model = AlunoModel()

def valid_data_student(data):
    required_fields = ["nome", "idade"]
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"O campo {field} é obrigatório."
    if not isinstance(data["idade"], int) or data["idade"] <= 0:
        return False, "O campo 'idade' deve ser um número inteiro positivo."
    return True, ""

@app.route('/alunos', methods=['GET'])
def get_alunos():
    return alunos_model.get_alunos()

@app.route('/alunos/<int:aluno_id>', methods=['GET'])
def get_aluno(aluno_id):
    return alunos_model.get_aluno(aluno_id)

@app.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.json
    return alunos_model.create_aluno(data)

@app.route('/alunos/<int:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    data = request.json
    return alunos_model.update_aluno(aluno_id, data)

@app.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    for aluno in alunos:
        if aluno['id'] == aluno_id:
            alunos.remove(aluno)
            return jsonify({"message": "Aluno deletado com sucesso!"})
    return jsonify({"error": "aluno não encontrado"}), 404


@app.route('/professores', methods=['GET'])
def get_professores():
    data = professores
    if data is None:
        return jsonify([])
    return jsonify(professores)


@app.route('/professor/<int:professor_id>', methods=['GET'])
def get_professor(professor_id):
    for professor in professores:
        if professor['id'] == professor_id:
            return jsonify({
                'professor': professor
            })

    return jsonify({'error': 'professor nao encontrado'}), 404


@app.route('/professor', methods=['POST'])
def create_professor():
    data = request.json
    if 'nome' not in data:
        return jsonify({'error': 'nome é um campo obrigatório'}), 400

    if 'disciplina' not in data:
        return jsonify({'error': 'disciplina é um campo obrigatório'}), 400

    professor = {
        'id': len(professores) + 1,
        'nome': data['nome'],
        'disciplina': data['disciplina']
    }
    professores.append(professor)
    return jsonify({
        'message': 'professor criado com sucesso',
        'professor': professor
    })


@app.route('/professor/<int:professor_id>', methods=['PUT'])
def update_professor(professor_id):
    for professor in professores:
        if professor['id'] == professor_id:
            data = request.json
            if 'nome' not in data:
                return jsonify({'error': 'nome é um campo obrigatório'}), 400

            if 'disciplina' not in data:
                return jsonify({'error': 'disciplina é um campo obrigatório'}), 400

            professor.update(data)
            return jsonify({
                'message': 'professor atualizado com sucesso',
                'professor': professor
            })

    return jsonify({'error': 'professor nao encontrado'}), 404

@app.route('/professor/<int:professor_id>', methods=['DELETE'])
def delete_professor(professor_id):
    for professor in professores:
        if professor['id'] == professor_id:
            professores.remove(professor)
            return jsonify({
                'message': 'professor removido com sucesso'
            })

    return jsonify({'error': 'professor nao encontrado'}), 404

@app.route('/turmas', methods=['GET'])
def get_turmas():
    data = turmas
    if data is None:
        return jsonify([])
    return jsonify(turmas)

@app.route('/turma/<int:turma_id>', methods=['GET'])
def get_turma(turma_id):
    for turma in turmas:
        if turma['id'] == turma_id:
            return jsonify({
                'turma': turma
            }), 200

    return jsonify({'error': 'turma nao encontrada'}), 404

@app.route('/turma', methods=['POST'])
def create_turma():
    data = request.json
    if 'nome' not in data:
        return jsonify({'error': 'nome é um campo obrigatório'}), 400

    if 'id_professor' not in data:
        return jsonify({'error': 'id_professor é um campo obrigatório'}), 400

    for professor in professores:
        if professor['id'] == data['id_professor']:
            turma = {
                'id': len(turmas) + 1,
                'nome': data['nome'],
                'id_professor': data['id_professor']
            }
            turmas.append(turma)
            return jsonify({
                'message': 'turma criada com sucesso',
                'turma': turma
            }), 200
    return jsonify({'error': f'professor {data['id_professor']} nao encontrado'}), 404

@app.route('/turma/<int:turma_id>', methods=['PUT'])
def update_turma(turma_id):
    for turma in turmas:
        if turma['id'] == turma_id:
            data = request.json
            if 'nome' not in data:
                return jsonify({'error': 'nome é um campo obrigatório'}), 400

            if 'id_professor' not in data:
                return jsonify({'error': 'id_professor é um campo obrigatório'}), 400

            for professor in professores:
                if professor['id'] == data['id_professor']:
                    turma = {
                        'nome': data['nome'],
                        'id_professor': data['id_professor']
                    }
                    turma.update(turma)
                    return jsonify({
                        'message': 'turma atualizada com sucesso',
                        'turma': turma
                    }), 200
            return jsonify({'error': f'professor {data['id_professor']} nao encontrado'}), 404
    return jsonify({'error': 'turma nao encontrada'}), 404

@app.route('/turma/<int:turma_id>', methods=['DELETE'])
def delete_turma(turma_id):
    for turma in turmas:
        if turma['id'] == turma_id:
            turmas.remove(turma)
            return jsonify({
                'message': 'turma removida com sucesso'
            })

    return jsonify({'error': 'turma nao encontrada'}), 404

@app.route('/turma/adiciona-aluno/<int:turma_id>/<int:aluno_id>', methods=['POST'])
def cadastra_aluno_turma(turma_id, aluno_id):
    aluno = next((a for a in alunos if a['id'] == aluno_id), None)
    turma = next((a for a in turmas if a['id'] == turma_id), None)
    print(aluno, turma)
    if not aluno in alunos:
        return jsonify({'error': 'aluno nao encontrado'}), 404
    if not turma in turmas:
        return jsonify({'error': 'turma nao encontrado'}), 404

    aluno["turma_id"] = turma_id

    aluno.update(aluno)
    return jsonify({
        'message': f'aluno cadastrado com sucesso na turma {turma_id}'
    })

if __name__ == '__main__':
    app.run(debug=True)