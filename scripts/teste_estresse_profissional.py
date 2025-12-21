# scripts/teste_estresse_profissional.py
import requests
import json

BASE_URL = "http://127.0.0.1:5001" # Certifique-se que o app.py está nesta porta

def executar_testes():
    print("=== INICIANDO ESCUDO DE QUALIDADE (FASE 3) ===\n")

    # TESTE 1: TENTANDO QUEBRAR O PORTEIRO (DADO INVÁLIDO)
    print("1. Testando Blindagem (Enviando JSON sem horário)...")
    lixo = {"id_cliente": 1, "data": "2025-12-20"} # Falta o horário
    res = requests.post(f"{BASE_URL}/agendar", json=lixo)
    if res.status_code == 400:
        print("✅ SUCESSO: O porteiro barrou o dado incompleto.\n")
    else:
        print(f"❌ FALHA: O sistema aceitou lixo! Status: {res.status_code}\n")

    # TESTE 2: CONFLITO NO MESMO BARBEIRO
    print("2. Testando Colisão (Mesmo Barbeiro, Mesmo Horário)...")
    pedido_1 = {"id_cliente": 1, "data": "2025-12-20", "horario": "14:00", "id_barbeiro": 1}
    
    # Primeiro agendamento (deve passar)
    requests.post(f"{BASE_URL}/agendar", json=pedido_1)
    
    # Segundo agendamento igual (deve falhar)
    res_conflito = requests.post(f"{BASE_URL}/agendar", json=pedido_1)
    if res_conflito.status_code == 409:
        print("✅ SUCESSO: Colisão detectada e bloqueada corretamente.\n")
    else:
        print(f"❌ FALHA: O sistema permitiu agendamento duplicado! Status: {res_conflito.status_code}\n")

    # TESTE 3: MULTI-BARBEIRO (O CÉREBRO EVOLUÍDO)
    print("3. Testando Multi-Barbeiro (Mesmo Horário, Barbeiros Diferentes)...")
    pedido_2 = {"id_cliente": 2, "data": "2025-12-20", "horario": "14:00", "id_barbeiro": 2}
    res_multi = requests.post(f"{BASE_URL}/agendar", json=pedido_2)
    
    if res_multi.status_code == 201:
        print("✅ SUCESSO: O sistema permitiu agendamentos simultâneos para profissionais diferentes.\n")
    else:
        print(f"❌ FALHA: O sistema bloqueou um barbeiro injustamente! Status: {res_multi.status_code}\n")

if __name__ == "__main__":
    try:
        executar_testes()
    except Exception as e:
        print(f"ERRO CRÍTICO: O servidor está ligado? {e}")