# routes/clientes_routes.py
from flask import Blueprint, request, jsonify
from middlewares.validators import validar_novo_cliente
from services.database_manager import verificar_existencia_cliente, inserir_cliente

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['POST'])
def cadastrar_cliente():
    # 1. Receber o JSON cru
    dados_brutos = request.get_json()

    # 2. Módulo A: Validação e Sanitização
    # Se falhar, nem incomodamos o banco de dados.
    cliente_limpo, erros = validar_novo_cliente(dados_brutos)
    if erros:
        return jsonify({'erros': erros}), 400

    # 3. Módulo B: Lógica de Negócio (Unicidade)
    # Verifica se CPF ou Email já existem
    tipo_conflito = verificar_existencia_cliente(cliente_limpo['cpf'], cliente_limpo['email'])  # type: ignore
    if tipo_conflito:
        # Retorna 409 Conflict - Erro semântico preciso
        return jsonify({'erro': f"Já existe um cliente cadastrado com este {tipo_conflito}."}), 409

    # 4. Módulo C: Persistência
    sucesso = inserir_cliente(cliente_limpo)
    
    if sucesso:
        return jsonify({'mensagem': 'Cliente cadastrado com sucesso!'}), 201
    
    return jsonify({'erro': 'Erro interno ao tentar salvar o cliente.'}), 500