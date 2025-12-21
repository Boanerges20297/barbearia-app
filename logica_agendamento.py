def verificar_disponibilidade(agendamentos_existentes, novo_pedido):
    """
    Regra de Negócio: 
    Um agendamento é inválido se houver colisão de (DATA + HORARIO + BARBEIRO).
    Barbeiros diferentes podem trabalhar no mesmo horário.
    """
    
    # Vamos padronizar para string para evitar erros de comparação (int vs str)
    novo_barbeiro = str(novo_pedido['id_barbeiro'])
    novo_horario = str(novo_pedido['horario'])
    nova_data = str(novo_pedido['data'])

    for agenda in agendamentos_existentes:
        # Padroniza os dados do banco/lista também
        agenda_barbeiro = str(agenda.get('id_barbeiro'))
        agenda_horario = str(agenda.get('horario'))
        agenda_data = str(agenda.get('data'))

        # A Lógica "E" (AND) - Todas as 3 condições devem ser verdadeiras para haver colisão
        mesmo_dia = (agenda_data == nova_data)
        mesmo_horario = (agenda_horario == novo_horario)
        mesmo_barbeiro = (agenda_barbeiro == novo_barbeiro)

        if mesmo_dia and mesmo_horario and mesmo_barbeiro:
            return {
                "aprovado": False, 
                "razao": f"O barbeiro {novo_barbeiro} já possui agendamento as {novo_horario}."
            }

    # Se passou por todos sem colidir:
    return {"aprovado": True, "razao": None}