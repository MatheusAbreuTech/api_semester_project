from flask import jsonify
from database.professores import professores
from professor.professor_model import Professor
from turma.turma_model import Turma
from aluno.aluno_model import Aluno


class TurmaService:
    def valid_data_class(self, data):
        if 'nome' not in data:
            return False, 'nome é um campo obrigatório'
        
    def get_turmas(self):
        try:
            turmas=Turma.query.all()
            return [turma.to_json() for turma in turmas], 200
        except Exception as e:
            return jsonify({"error":f"Erro ao buscar turmas: {str(e)}"}), 500

    def get_turma(self, turma_id):
        try:
            turma = Turma.query.get(turma_id)
            if not turma:
                return jsonify({'error': 'turma nao encontrada'}), 404
            return turma.to_json(), 200
        except Exception as e:
            return jsonify({"error":f"Erro ao buscar turma: {str(e)}"}), 500
        
    def create_turma(self, data):
        valid, msg = self.valid_data_class(data)
        if not valid:
            return jsonify({'error': msg}), 400
        try:
            turma = Turma(**data)
            db.session.add(turma)
            db.session.commit()
            return jsonify({
                'message': 'turma criada com sucesso',
                'turma': turma.to_json()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Erro ao criar turma: {str(e)}'}), 500
        
    def update_turma(self, turma_id, data):
        try:
            turma = Turma.query.get(turma_id)
            if not turma:
                return jsonify({'error': 'turma nao encontrada'}), 404
            for key, value in data.items():
                setattr(turma, key, value)
            db.session.commit()
            return jsonify({
                'message': 'turma atualizada com sucesso',
                'turma': turma.to_json()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Erro ao atualizar turma: {str(e)}'}), 500

    def delete_turma(self, turma_id):
        try:
            turma = Turma.query.get(turma_id)
            if not turma:
                return jsonify({'error': 'turma nao encontrada'}), 404
            db.session.delete(turma)
            db.session.commit()
            return jsonify({'message': 'turma deletada com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Erro ao deletar turma: {str(e)}'}), 500
        
    def add_student(self, turma_id, aluno_id):
        try:
            query=(
               update(Aluno)
               .where(id == aluno_id)
               .values(turma_id=turma_id)
            )

            aluno=Aluno.query.get(aluno_id)
            if not aluno:
                return jsonify({'error': 'aluno nao encontrado'}), 404
            turma = Turma.query.get(turma_id)
            if not turma:
                return jsonify({'error': 'turma nao encontrada'}), 404
            if turma_id in aluno.to_json()['turma_id']:  # Verifica se o aluno ja esta na turma
                return jsonify({'error': 'aluno ja esta na turma'}), 400
            db.session.execute(query)
            db.session.commit()
            return jsonify({'message': 'aluno adicionado a turma com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Erro ao adicionar aluno a turma: {str(e)}'}), 500

            
    def remove_student(self, turma_id, aluno_id):
       try:
            query=(
               update(Aluno)
               .where(id == aluno_id)
               .values(turma_id=None)
            )

            aluno=Aluno.query.get(aluno_id)
            if not aluno:
                return jsonify({'error': 'aluno nao encontrado'}), 404
            turma = Turma.query.get(turma_id)
            if not turma:
                return jsonify({'error': 'turma nao encontrada'}), 404
            db.session.execute(query)
            db.session.commit()
            return({'message': 'Aluno removido com sucesso'})
       except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Erro ao remover aluno: {str(e)}'}), 500

       
       
    def add_professor(self, turma_id, professor_id):
        try:
            query=(
                update(Turma)
                .where(id==turma_id)
                .values(professor_id=professor_id)
            )

            professor=Professor.query.get(professor_id)
            if not professor:
                return jsonify({'error': 'Professor nao encontrado'}), 404
            turma=Turma.query.get(turma_id)
            if not turma:
                return jsonify({'error': 'turma nao encontrada'}), 404
            
            db.session.execute(query)
            db.session.commit()
            return jsonify({'message': 'Professor adicionado a turma com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Erro ao adicionar Professor a turma: {str(e)}'}), 500
        



        
            
            