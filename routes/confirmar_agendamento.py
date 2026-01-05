import json
from flask import Blueprint, jsonify, request
from middlewares.validators import identificar_e_validar_autor
from services.database_manager import confirmar_agendamento

confirmar_agendamento_bp = Blueprint('confirmar_agendamento', __name__)

@confirmar_agendamento_bp.route('/confirmar-agendamento/<int:id_agendamento>', methods = ['PUT'])
def confirmar(id_agendamento):
    
    id_barbeiro, tipo_autor, erro = identificar_e_validar_autor(request.headers)
    
    if erro:
        return {"erro": erro}, 401
    
    if tipo_autor != "barbeiro":
        return {"erro": "Você não tem permissão para essa ação."}, 401
    
    sucesso = confirmar_agendamento(id_agendamento,id_barbeiro)
    
    if sucesso:
        return jsonify({"mensagem":"Agendamento confirmado com sucesso."}),200
    
    return jsonify({"erro": "Não foi possível confirmar. Verifique se o ID existe ou já foi confirmado."}), 404