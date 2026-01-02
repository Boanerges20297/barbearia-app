import json
from flask import Blueprint, jsonify, request
from services.database_manager import deletar_agendamento

deletar_agendamento_bp = Blueprint('deletar_agendamento', __name__)

@deletar_agendamento_bp.route('/deletar-agendamento/<int:id_agendamento>', methods = ['DELETE'])
def deletar(id_agendamento):
    
    id_barbeiro = request.headers.get('X-Barbeiro-ID')
    
    if not id_barbeiro:
        return jsonify({"erro": "Identificação do barbeiro ausente"}), 401
    
    try:
        result = deletar_agendamento(id_agendamento,id_barbeiro)
        
        if result:
            return jsonify({"mensagem":"Agendamento apagado com sucesso."}),200
        else:
            return jsonify({"erro": "Agendamento não encontrado, já confirmado ou você não tem permissão"}), 404
    except Exception as e:
        print(f"Erro ao deletar agendamento - {e}")
        return jsonify({"erro": "Erro interno"}), 500    
    
    