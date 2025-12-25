from flask import Blueprint, request, jsonify
from database_manager import ler_todos_agendamentos, inserir_agendamento
from logica_agendamento import verificar_disponibilidade
# Importação limpa do novo módulo
from validators import sanitizar_e_validar_pedido

agendamento_bp = Blueprint('agendamento', __name__)

@agendamento_bp.route('/agendamentos', methods=['GET'])
def listar():
    # ... (o teu código atual mantém-se igual) ...
    try:
        lista = ler_todos_agendamentos()
        return jsonify(lista), 200
    except Exception as e:
        print(f"Erro ao listar: {e}")
        return jsonify({"erro": "Erro interno"}), 500

@agendamento_bp.route('/agendar', methods=['POST'])
def criar():
    try:
        dados_brutos = request.get_json()
        # Uso da função importada
        pedido_limpo, erros = sanitizar_e_validar_pedido(dados_brutos)
        
        if erros or pedido_limpo is None:
            return jsonify({"erro": "Dados inválidos", "detalhes": erros}), 400

        agendamentos_existentes = ler_todos_agendamentos()
        resultado = verificar_disponibilidade(agendamentos_existentes, pedido_limpo)
        
        if not resultado['aprovado']:
             return jsonify({"erro": "Conflito", "motivo": resultado['razao']}), 409

        inserir_agendamento(
            pedido_limpo['id_cliente'],
            pedido_limpo['data'],
            pedido_limpo['horario'],
            pedido_limpo['id_barbeiro'],
            pedido_limpo['id_servico']
        )
        return jsonify({"mensagem": "Sucesso", "dados": pedido_limpo}), 201

    except Exception as e:
        print(f"Erro no POST: {e}")
        return jsonify({"erro": "Erro interno"}), 500