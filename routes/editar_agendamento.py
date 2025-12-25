# Abaixo, importamos os módulos do flask (Blueprint, request, jsonify)
from flask import Blueprint, request, jsonify
# Importações explícitas (Boa prática: saber de onde vem cada função)
# Abaixo, importamos de database_manager e logica_agendamento as necessários
from database_manager import editar_agendamento, ler_todos_agendamentos
from logica_agendamento import verificar_disponibilidade
# Reutilização de função de sanitização e validação, vindas de agendamentos_routes.py
from agendamentos_routes import sanitizar_e_validar_pedido
from routes import agendamentos_routes

# Abaixo, criamos um Blueprint específico para edição de agendamentos
editar_agendamento_bp = Blueprint("editar_agendamento", __name__)

# --- ROTA: Editar Agendamento ---
@editar_agendamento_bp.route('editar-agendamento/<int:id_agendamento>', methods = ['PUT'])
# Função para editar um agendamento existente
def editar(id_agendamento):
    # Obter os dados brutos do pedido
    dados_brutos = request.get_json()
    # 1. Sanitização e Validação do Pedido
    # Chama a função reutilizável para sanitizar e validar, de agendamentos_routes.py
    pedido_limpo, erros = sanitizar_e_validar_pedido(dados_brutos)
    # Se houver erros de validação, retornar imediatamente
    if erros:
        return jsonify({"erros": erros}), 400
    # 2. Verificação de Disponibilidade
    agendamentos_existentes = ler_todos_agendamentos()
    # Remover o agendamento atual da lista para evitar conflito consigo mesmo
    agendamentos_filtrados = [ag for ag in agendamentos_existentes if ag['id'] != id_agendamento]
    # Verificar se o novo agendamento conflita com os existentes
    disponibilidade = verificar_disponibilidade(agendamentos_filtrados, pedido_limpo)
    # Se não estiver disponível, retornar erro
    if not disponibilidade['aprovado']:
        return jsonify({"erros": disponibilidade['razao']}), 409
    # 3. Atualização no Banco de Dados
    # Aqui fazemos a chamada para atualizar o agendamento no banco
    try:
        # Chamada à função de edição no database_manager.py
        editar_agendamento(id_agendamento, pedido_limpo)
        # Retornar sucesso
        return jsonify({"mensagem": "Agendamento atualizado com sucesso."}), 200
    # Captura qualquer erro inesperado (Banco fora do ar, bug no código, etc)
    except Exception as e:
        # Logar o erro real no console para o desenvolvedor
        print(f"Erro ao editar agendamento: {e}")
        # Retornar erro genérico para o cliente
        return jsonify({"erro": "Erro interno ao atualizar agendamento."}),500
    
        
        
    
        

    
    
    


