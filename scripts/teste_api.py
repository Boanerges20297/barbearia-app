# teste_api.py
import requests
import json

BASE_URL = "http://127.0.0.1:5002"

def testar():
    print("--- 1. Testando Listagem (GET) ---")
    try:
        response = requests.get(f"{BASE_URL}/agendamentos")
        print(f"Status: {response.status_code}")
        print(f"Dados: {response.json()}")
    except Exception as e:
        print(f"ERRO NO GET: {e}")

    print("\n--- 2. Testando Agendamento Novo (POST) ---")
    novo_pedido = {
        "id_cliente": 1,
        "data": "2025-02-20",
        "horario": "15:00"
    }
    try:
        response = requests.post(f"{BASE_URL}/agendar", json=novo_pedido)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
    except Exception as e:
        print(f"ERRO NO POST: {e}")

    print("\n--- 3. Testando Conflito de Horário (POST Repetido) ---")
    # Tentamos agendar EXATAMENTE o mesmo horário
    try:
        response = requests.post(f"{BASE_URL}/agendar", json=novo_pedido)
        print(f"Status: {response.status_code} (Esperado: 409)")
        print(f"Resposta: {response.json()}")
    except Exception as e:
        print(f"ERRO NO POST REPETIDO: {e}")

if __name__ == "__main__":
    testar()