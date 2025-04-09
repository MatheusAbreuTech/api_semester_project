from flask import  jsonify, request
from config import app
from aluno.aluno_controller import alunos_blueprint
from database.alunos import alunos
from database.professores import professores
from database.turmas import turmas

app.register_blueprint(alunos_blueprint)

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
def cadastra_aluno_bturma(turma_id, aluno_id):
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
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )