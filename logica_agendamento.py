def verificar_disponibilidade(agendamentos_existentes, novo_pedido):
    """
    Verifica se há conflito de agenda.
    Regra: (Mesmo Dia) AND (Mesmo Horário) AND (Mesmo Barbeiro) = Conflito.
    """
    
    # 1. Normalização de Entrada (Casting para garantir comparação exata)
    novo_barbeiro = str(novo_pedido['id_barbeiro'])
    novo_horario = str(novo_pedido['horario'])
    nova_data = str(novo_pedido['data'])

    for agenda in agendamentos_existentes:
        # 2. Normalização dos dados armazenados
        agenda_barbeiro = str(agenda.get('id_barbeiro', '0')) # Valor padrão '0' se não existir
        agenda_horario = str(agenda.get('horario'))
        agenda_data = str(agenda.get('data'))

        # 3. Verificação de Colisão Atômica
        colisao = (
            agenda_data == nova_data and 
            agenda_horario == novo_horario and 
            agenda_barbeiro == novo_barbeiro
        )

        if colisao:
            return {
                "aprovado": False, 
                "razao": f"O barbeiro {novo_barbeiro} já está ocupado às {novo_horario}."
            }

    # Se o loop terminar sem retornos, está livre
    return {"aprovado": True, "razao": None}