from flask import Blueprint, jsonify, request
from database.alunos import alunos

from database.turmas import turmas

turmas_blueprint = Blueprint('turmas', __name__)


@turmas_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    data = turmas
    if data is None:
        return jsonify([])
    return jsonify(turmas)


@turmas_blueprint.route('/turma/<int:turma_id>', methods=['GET'])
def get_turma(turma_id):
    for turma in turmas:
        if turma['id'] == turma_id:
            return jsonify({
                'turma': turma
            })

    return jsonify({'error': 'turma nao encontrado'}), 404


@turmas_blueprint.route('/turma', methods=['POST'])
def create_turma():
    data = request.json
    if 'nome' not in data:
        return jsonify({'error': 'nome é um campo obrigatório'}), 400

    if 'disciplina' not in data:
        return jsonify({'error': 'disciplina é um campo obrigatório'}), 400

    turma = {
        'id': len(turmas) + 1,
        'nome': data['nome'],
        'disciplina': data['disciplina']
    }
    turmas.append(turma)
    return jsonify({
        'message': 'turma criado com sucesso',
        'turma': turma
    })


@turmas_blueprint.route('/turma/<int:turma_id>', methods=['PUT'])
def update_turma(turma_id):
    for turma in turmas:
        if turma['id'] == turma_id:
            data = request.json
            if 'nome' not in data:
                return jsonify({'error': 'nome é um campo obrigatório'}), 400

            if 'professor' not in data:
                return jsonify({'error': 'professor é um campo obrigatório'}), 400

            turma["nome"] = data['nome']
            turma["professor"] = data['professor']
            return jsonify({
                'message': 'turma atualizada com sucesso',
                'turma': turma
            })

    return jsonify({'error': 'turma nao encontrado'}), 404


@turmas_blueprint.route('/turma/<int:turma_id>', methods=['DELETE'])
def delete_turma(turma_id):
    for turma in turmas:
        if turma['id'] == turma_id:
            turmas.remove(turma)
            return jsonify({
                'message': 'turma removido com sucesso'
            })

    return jsonify({'error': 'turma nao encontrado'}), 404


@turmas_blueprint.route('/turma/<int:turma_id>', methods=['GET'])
def get_alunos_por_turma(turma_id):
    for aluno in alunos:
        if aluno['turma_id'] == turma_id:
            return jsonify({
                'turma': turma
            })

    return jsonify({'error': 'turma nao encontrado'}), 404



@turmas_blueprint.route('/turma/adiciona-aluno/<int:turma_id>/<int:aluno_id>',methods=['POST'])
def cadastra_aluno_turma(turma_id,aluno_id):
    aluno = next((a for a in alunos if a ['id'] == aluno_id), None)
    turma = next((a for a in turmas if a ['id'] == turma_id), None)
    print(aluno,turma)
    if not aluno in alunos:
        return jsonify({'error': 'aluno nao encontrado'}), 404
    if not turma in turmas:
        return jsonify({'error': 'turma nao encontrado'}), 404
#    TO DO LIST
#    criar verificação se aluno ja esta em turma
    
    aluno["turma_id"] = turma_id
    
    aluno.update(aluno)
    return jsonify({
        'message': f'aluno cadastrado com sucesso na turma {turma_id}'
    })

    