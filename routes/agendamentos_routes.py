from asyncio.windows_events import NULL
from datetime import date
from flask import Blueprint, request, jsonify
import sys           # 1. Chame o gerente do sistema
sys.path.append("..") # 2. Adicione o diretório pai ("..") à lista de lugares onde o Python procura arquivos
from database_manager import ler_todos_agendamentos, inserir_agendamento
from logica_agendamento import verificar_disponibilidade

# Definindo o "Departamento"
agendamento_bp = Blueprint('agendamento', __name__)

def validar_input_agendamentos(dados):
    campos_obrigatorios = ['id_cliente', 'data','horario']
    # 1. Verifica se todos os campos existem e não estão vazios
    for campo in campos_obrigatorios:
        if campo not in dados or not str(dados[campo].strip()):
            return False, f"O campo '{campo}' é obrigatório e não pode estar vazio."


    # 2. verifica se o id_cliente é um número inteiro positivo
    if not str(dados['id_cliente']).isdigit():
        return False, "O 'id_cliente' deve ser um número inteiro positivo."
    
    return True, None


# Note que usamos @agendamento_bp.route em vez de @app.route
@agendamento_bp.route('/agendamentos', methods=['GET'])
def listar():
    lista = ler_todos_agendamentos()
    return jsonify(lista)

@agendamento_bp.route('/agendar', methods=['POST'])
def criar():
    data = request.json
    
    # --- A BLINDAGEM ACONTECE AQUI ---
    sucesso, mensagem_erro = validar_input_agendamentos(data)
    if not sucesso:
        return jsonify({"erro": "Dados inválidos", "detalhes": mensagem_erro}), 400
    # ---------------------------------
    
    pedido_completo = {
        "id_cliente": data.get('id_cliente') or 0,
        "horario": data.get('horario') or '00:00',
        "data": data.get('data', '2025-01-01') or date.today().isoformat(),
        "id_barbeiro": data.get('id_barbeiro', 1),
        "id_servico": data.get('id_servico', 1)
    }

    agendamentos_existentes = ler_todos_agendamentos()
    resultado = verificar_disponibilidade(agendamentos_existentes, pedido_completo)

    if resultado['aprovado']:
        inserir_agendamento(
            pedido_completo['id_cliente'], 
            pedido_completo['data'], 
            pedido_completo['horario'],
            pedido_completo['id_barbeiro'],
            pedido_completo['id_servico']
        )
        return jsonify({"mensagem": "Sucesso!", "detalhes": pedido_completo}), 201
    else:
        return jsonify({"erro": resultado['razao']}), 409