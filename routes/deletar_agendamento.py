import json
from flask import Blueprint, jsonify, request
from services.database_manager import deletar_agendamento
from middlewares.validators import identificar_e_validar_autor

deletar_agendamento_bp = Blueprint('deletar_agendamento', __name__)

@deletar_agendamento_bp.route('/deletar-agendamento/<int:id_agendamento>', methods = ['DELETE'])
def deletar(id_agendamento):
    
    id_autor, tipo_autor, erro_autor = identificar_e_validar_autor(request.headers)
    if erro_autor:
        return jsonify({"erro": erro_autor}), 401
    
    sucesso = deletar_agendamento(id_agendamento,id_autor, tipo_autor)
    
    if sucesso:
        return jsonify({"mensagem":"Agendamento apagado com sucesso."}),200
    
    return jsonify({"erro": "Não foi possível confirmar. Verifique se o ID existe ou já foi confirmado."}), 404