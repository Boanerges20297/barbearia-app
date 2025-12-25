from flask import Blueprint, request, jsonify
from database_manager import editar_agendamento, ler_todos_agendamentos
from logica_agendamento import verificar_disponibilidade
# Importação limpa
from middlewares.validators import sanitizar_e_validar_pedido

editar_agendamento_bp = Blueprint("editar_agendamento", __name__)

@editar_agendamento_bp.route('/editar-agendamento/<int:id_agendamento>', methods=['PUT'])
def editar(id_agendamento):
    dados_brutos = request.get_json()
    
    # Validamos como update (opcionalmente podes passar is_update=True se mudares a lógica)
    pedido_limpo, erros = sanitizar_e_validar_pedido(dados_brutos)
    
    if erros:
        return jsonify({"erros": erros}), 400
        
    # ... Lógica de disponibilidade e update (mantém-se a tua) ...
    try:
        agendamentos_existentes = ler_todos_agendamentos()
        # Filtra o próprio agendamento para não conflitar consigo mesmo
        outros_agendamentos = [ag for ag in agendamentos_existentes if ag['id'] != id_agendamento]
        
        disponibilidade = verificar_disponibilidade(outros_agendamentos, pedido_limpo)
        if not disponibilidade['aprovado']:
            return jsonify({"erros": disponibilidade['razao']}), 409
            
        editar_agendamento(id_agendamento, pedido_limpo)
        return jsonify({"mensagem": "Atualizado com sucesso"}), 200
        
    except Exception as e:
        print(f"Erro ao editar: {e}")
        return jsonify({"erro": "Erro interno"}), 500