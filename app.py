from flask import Flask, jsonify

app = Flask(__name__)

professores = [
        {"id": 1, "nome": "Ana Silva", "disciplina": "Matemática"},
        {"id": 2, "nome": "Carlos Souza", "disciplina": "História"},
        {"id": 3, "nome": "Fernanda Costa", "disciplina": "Biologia"}
    ]

alunos =  [
        {"id": 1, "nome": "João Pereira", "idade": 15, "turma_id": 101},
        {"id": 2, "nome": "Mariana Lima", "idade": 14, "turma_id": 101},
        {"id": 3, "nome": "Lucas Oliveira", "idade": 16, "turma_id": 102},
        {"id": 4, "nome": "Beatriz Santos", "idade": 15, "turma_id": 103},
        {"id": 5, "nome": "Gabriel Martins", "idade": 14, "turma_id": 103}
    ]

turmas = [
        {"id": 101, "nome": "Turma A", "ano": 2024, "professor_id": 1},
        {"id": 102, "nome": "Turma B", "ano": 2024, "professor_id": 2},
        {"id": 103, "nome": "Turma C", "ano": 2024, "professor_id": 3}
    ],

@app.route('/teachers')
def hello_world():
    return jsonify({'professores': professores})

if __name__ == '__main__':
    app.run()
