from flask import Blueprint, request, jsonify
from services.database_manager import editar_agendamento, ler_todos_agendamentos
from services.logica_agendamento import verificar_disponibilidade
# Importação limpa
from middlewares.validators import sanitizar_e_validar_pedido, identificar_e_validar_autor

editar_agendamento_bp = Blueprint("editar_agendamento", __name__)

@editar_agendamento_bp.route('/editar-agendamento/<int:id_agendamento>', methods=['PUT'])
def editar(id_agendamento):
    # 1. Identifica e Valida quem está chamando (Módulo A/B)
    id_autor, tipo_autor, erro_autor = identificar_e_validar_autor(request.headers)
    if erro_autor:
        return jsonify({"erro": erro_autor}), 401

    # 2. Valida o corpo do pedido (Módulo B)
    dados_brutos = request.get_json()
    pedido_limpo, erros_dados = sanitizar_e_validar_pedido(dados_brutos, is_update=True)
    if erros_dados:
        return jsonify({"erros": erros_dados}), 400

    try:
        # 3. Lógica de Conflito (Agnóstica)
        agendamentos_existentes = ler_todos_agendamentos()
        outros = [ag for ag in agendamentos_existentes if ag['id'] != id_agendamento]
        
        disponibilidade = verificar_disponibilidade(outros, pedido_limpo)
        if not disponibilidade['aprovado']:
            return jsonify({"erro": disponibilidade['razao']}), 409

        # 4. Persistência com Trava de Autor (Módulo C)
        sucesso = editar_agendamento(id_agendamento, pedido_limpo, id_autor, tipo_autor)
        
        if sucesso:
            return jsonify({"mensagem": "Atualizado com sucesso"}), 200
        
        return jsonify({"erro": "Não autorizado ou agendamento já confirmado."}), 403

    except Exception as e:
        return jsonify({"erro": "Erro interno"}), 500