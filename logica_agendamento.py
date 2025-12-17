# logica_agendamento.py

def verificar_disponibilidade(agendamentos_existentes, novo_pedido):
    """
    Módulo B: Lógica Pura
    Responsabilidade: Verificar se há colisão de horário.
    Input: 
        - agendamentos_existentes: Lista de dicionários [{'horario': '14:00'}, ...]
        - novo_pedido: Dicionário {'horario': '14:00'}
    Output:
        - Dicionário {'aprovado': bool, 'razao': str}
    """
    
    # 1. Extraia o horário desejado do novo_pedido
    data_desejada = novo_pedido.get('data')
    horario_desejado = novo_pedido.get('horario')
    
    if not horario_desejado or not data_desejada:
        return {"aprovado": False, "razao": "Data e Horário são obrigatórios."}
    
    # 2. Itere sobre a lista de agendamentos_existentes
    # SE encontrar um horário igual ao desejado -> Retorne Erro
    
    for h in agendamentos_existentes:
        if(horario_desejado == h['horario'] and data_desejada == h['data']):
            return {"aprovado": False, "razao": "Data ou Horário indisponível"}
    
    # 3. Se o loop terminar sem colisão -> Retorne Sucesso
    return {"aprovado": True, "razao": "Horário disponível"}

