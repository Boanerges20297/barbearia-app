# logica_agendamento.py

def verificar_disponibilidade(agendamentos_existentes, novo_pedido):
    """
    Módulo B: Lógica Pura (Evoluída)
    Responsabilidade: Verificar colisão por BARBEIRO.
    """
    
    data_desejada = novo_pedido.get('data')
    horario_desejado = novo_pedido.get('horario')
    barbeiro_desejado = novo_pedido.get('id_barbeiro')
    
    # 1. Validação de Sanidade (Cérebro não processa dados incompletos)
    if not all([data_desejada, horario_desejado, barbeiro_desejado]):
        return {"aprovado": False, "razao": "Dados insuficientes para marcar agendamento."}
    
    # 2. Busca por conflito específico
    for agendamento in agendamentos_existentes:
        mesmo_horario = agendamento['horario'] == horario_desejado
        mesma_data = agendamento['data'] == data_desejada
        mesmo_barbeiro = agendamento['id_barbeiro'] == barbeiro_desejado
        
        if mesmo_horario and mesma_data and mesmo_barbeiro:
            return {
                "aprovado": False, 
                "razao": f"O barbeiro {barbeiro_desejado} já possui cliente neste horário."
            }
    
    return {"aprovado": True, "razao": "Horário disponível para este profissional."}