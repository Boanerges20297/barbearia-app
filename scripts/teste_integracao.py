import requests
import json

BASE_URL = "http://127.0.0.1:5000/agendar"

def testar_api():
    print("--- INICIANDO TESTES DE INTEGRAÇÃO ---\n")

    # --- TESTE 1: Caminho Feliz (Sucesso) ---
    payload_sucesso = {"horario": "16:00", "id_cliente": 99}
    print(f"1. Tentando agendar às {payload_sucesso['horario']}...")
    
    try:
        response = requests.post(BASE_URL, json=payload_sucesso)
        
        if response.status_code == 201:
            print(f"✅ SUCESSO! Código: {response.status_code}")
            print(f"   Resposta: {response.json()}\n")
        else:
            print(f"❌ FALHA INESPERADA. Código: {response.status_code}")
            print(f"   Resposta: {response.text}\n")
            
    except Exception as e:
        print(f"❌ ERRO DE CONEXÃO: {e}. O servidor app.py está rodando?\n")

    # --- TESTE 2: Teste de Colisão (Erro Esperado) ---
    # Vamos tentar agendar às 10:00 (que já existe no DB_MOCK)
    payload_erro = {"horario": "10:00", "id_cliente": 88}
    print(f"2. Tentando forçar colisão às {payload_erro['horario']}...")
    
    try:
        response = requests.post(BASE_URL, json=payload_erro)
        
        if response.status_code == 409:
            print(f"✅ SUCESSO NO BLOQUEIO! O sistema rejeitou corretamente.")
            print(f"   Código: {response.status_code}")
            print(f"   Motivo: {response.json()}\n")
        elif response.status_code == 201:
            print(f"❌ FALHA GRAVE: O sistema permitiu agendamento duplicado!\n")
        else:
            print(f"⚠️ Retorno inesperado: {response.status_code} - {response.text}\n")
            
    except Exception as e:
        print(f"❌ ERRO DE CONEXÃO: {e}")

if __name__ == "__main__":
    # Verifica se tem a lib requests, se não, avisa
    try:
        testar_api()
    except NameError:
        print("A biblioteca 'requests' não está instalada.")
        print("Rode no terminal: pip install requests")