from flask import Blueprint, request, jsonify
from datetime import date
import sys

# OBS: Em um projeto real, configuraríamos o PYTHONPATH no ambiente, 
# mas vou manter o sys.path documentado como débito técnico por enquanto.
sys.path.append("..") 

# Importações explicitas (Boa prática: saber de onde vem cada função)
from database_manager import ler_todos_agendamentos, inserir_agendamento
from logica_agendamento import verificar_disponibilidade

agendamento_bp = Blueprint('agendamento', __name__)

# --- MÓDULO A: Camada de Validação e Sanitização ---
def sanitizar_e_validar_pedido(dados_brutos):
    """
    Responsabilidade: Receber o lixo (input bruto), validar regras de tipo
    e devolver um objeto limpo e pronto para uso (dicionário confiável).
    """
    erros = []
    
    # 1. Validação de Presença (O que é obrigatório?)
    campos_obrigatorios = ['id_cliente', 'data', 'horario']
    for campo in campos_obrigatorios:
        if campo not in dados_brutos or not str(dados_brutos[campo]).strip():
            erros.append(f"O campo '{campo}' é obrigatório.")

    # Se já falhou aqui, retorna logo para não processar o resto à toa
    if erros:
        return None, erros

    # 2. Validação de Tipo (Type Safety)
    try:
        id_cliente = int(dados_brutos['id_cliente'])
        if id_cliente <= 0:
            erros.append("O 'id_cliente' deve ser positivo.")
    except (ValueError, TypeError):
        erros.append("O 'id_cliente' deve ser um número inteiro.")

    if erros:
        return None, erros

    # 3. Construção do Objeto Limpo (Sanitização)
    # Removemos a lógica de 'or' perigosa e usamos valores explícitos
    pedido_limpo = {
        "id_cliente": id_cliente, # type: ignore
        "data": dados_brutos['data'], # Já validamos que existe
        "horario": dados_brutos['horario'], # Já validamos que existe
        "id_barbeiro": dados_brutos.get('id_barbeiro', 1), # Default seguro
        "id_servico": dados_brutos.get('id_servico', 1)    # Default seguro
    }
    
    return pedido_limpo, None


# --- MÓDULO C: Rotas e Controle de Fluxo ---

@agendamento_bp.route('/agendamentos', methods=['GET'])
def listar():
    try:
        lista = ler_todos_agendamentos()
        return jsonify(lista), 200
    except Exception as e:
        # Logar o erro real no console para o desenvolvedor
        print(f"Erro ao listar agendamentos: {e}") 
        return jsonify({"erro": "Erro interno ao buscar dados."}), 500

@agendamento_bp.route('/agendar', methods=['POST'])
def criar():
    # Bloco de segurança principal
    try:
        dados_brutos = request.get_json()
        if not dados_brutos:
            return jsonify({"erro": "Payload JSON inválido ou vazio"}), 400

        # 1. Validação (Blindagem)
        pedido_completo, lista_erros = sanitizar_e_validar_pedido(dados_brutos)
        
        if lista_erros:
            return jsonify({"erro": "Dados inválidos", "detalhes": lista_erros}), 400

        # 2. Lógica de Negócio (Módulo B invocado)
        # Note como a rota não sabe COMO a disponibilidade é verificada, ela apenas pede.
        agendamentos_existentes = ler_todos_agendamentos()
        resultado = verificar_disponibilidade(agendamentos_existentes, pedido_completo)

        if not resultado['aprovado']:
            return jsonify({"erro": "Conflito de agenda", "motivo": resultado['razao']}), 409

        # 3. Persistência (Commit)
        inserir_agendamento(
            pedido_completo['id_cliente'],  # type: ignore
            pedido_completo['data'],  # type: ignore
            pedido_completo['horario'], # type: ignore
            pedido_completo['id_barbeiro'], # type: ignore
            pedido_completo['id_servico'] # type: ignore
        )
        
        return jsonify({
            "mensagem": "Agendamento realizado com sucesso", 
            "dados": pedido_completo
        }), 201

    except Exception as e:
        # Captura qualquer erro inesperado (Banco fora do ar, bug no código, etc)
        # Em produção, usaríamos uma lib de logging aqui.
        print(f"ERRO CRÍTICO NA ROTA /agendar: {e}")
        return jsonify({"erro": "Ocorreu um erro interno no servidor. Tente novamente mais tarde."}), 500