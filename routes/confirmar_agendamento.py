import json
from flask import Blueprint, jsonify, request
from services.database_manager import confirmar_agendamento

confirmar_agendamento_bp = Blueprint('confirmar_agendamento', __name__)

@confirmar_agendamento_bp.route('/confirmar-agendamento/<int:id_agendamento>', methods = ['PUT'])
def confirmar(id_agendamento):
    
    id_barbeiro = request.headers.get('X-Barbeiro-ID')
    
    if not id_barbeiro:
        return jsonify({"erro": "Identificação do barbeiro ausente"}), 401
    
    try:
        result = confirmar_agendamento(id_agendamento,id_barbeiro)
        
        if result:
            return jsonify({"mensagem":"Agendamento confirmado com sucesso."}),200
        else:
            return jsonify({"erro": "Agendamento não encontrado, já confirmado ou você não tem permissão"}), 404
    except Exception as e:
        print(f"Erro ao confirmar agendamento - {e}")
        return jsonify({"erro": "Erro interno"}), 500    
    
    