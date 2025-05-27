import requests

DISCIPLINA_SERVICE_URL = "http://atividade_service:5002/atividades/disciplina"

class DisciplinaServiceClient:
    @staticmethod
    def verificar_disciplina_existe(id_disciplina):
        url = f"{DISCIPLINA_SERVICE_URL}/{id_disciplina}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data if data.get('id') else False
        except requests.RequestException as e:
            print(f"Erro ao acessar a disciplina.service: {e}")
            return False