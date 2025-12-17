from flask import Blueprint, request, jsonify
import sys           # 1. Chame o gerente do sistema
sys.path.append("..") # 2. Adicione o diretório pai ("..") à lista de lugares onde o Python procura arquivos
from database_manager import ler_todos_agendamentos, inserir_agendamento
from logica_agendamento import verificar_disponibilidade

# Definindo o "Departamento"
agendamento_bp = Blueprint('agendamento', __name__)

# Note que usamos @agendamento_bp.route em vez de @app.route
@agendamento_bp.route('/agendamentos', methods=['GET'])
def listar():
    lista = ler_todos_agendamentos()
    return jsonify(lista)

@agendamento_bp.route('/agendar', methods=['POST'])
def criar():
    data = request.json
    
    pedido_completo = {
        "id_cliente": data.get('id_cliente'),
        "horario": data.get('horario'),
        "data": data.get('data', '2025-01-01'),
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