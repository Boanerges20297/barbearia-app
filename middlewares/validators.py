# === FUNÇÃO DE SANITIZAÇÃO E VALIDAÇÃO ===
# Esta função é responsável por limpar e validar os dados recebidos nas requisições
def sanitizar_e_validar_pedido(dados_brutos, is_update=False):
    """
    Valida e limpa os dados de entrada.
    param is_update: Se True, pode relaxar certas regras (ex: id_cliente) se necessário.
    """
    # Inicializa uma lista vazia para armazenar possíveis erros de validação
    erros = []
    
    # --- ETAPA 1: Definir Campos Obrigatórios ---
    # Define os campos mínimos necessários para um agendamento (data e horário são sempre obrigatórios)
    campos_obrigatorios = ['data', 'horario']
    
    # Verifica se é uma criação de agendamento (não é update)
    # Em criações novas, o id_cliente também é obrigatório
    if not is_update:
        campos_obrigatorios.append('id_cliente')

    # --- ETAPA 2: Validar Presença dos Campos Obrigatórios ---
    # Percorre cada campo obrigatório para verificar se existe e não está vazio
    for campo in campos_obrigatorios:
        # Verifica se o campo não existe OU se está vazio após remover espaços
        if campo not in dados_brutos or not str(dados_brutos[campo]).strip():
            # Adiciona mensagem de erro específica para o campo faltante
            erros.append(f"O campo '{campo}' é obrigatório.")

    # Se houver erros de campos obrigatórios, retorna imediatamente
    # Retorna None para os dados e a lista de erros encontrados
    if erros:
        return None, erros

    # --- ETAPA 3: Validação de Tipos e Valores ---
    # Extrai o id_cliente dos dados brutos (pode ser None se não existir)
    id_cliente = dados_brutos.get('id_cliente')
    
    # Valida o id_cliente apenas se ele foi fornecido
    if id_cliente is not None:
        try:
            # Tenta converter para número inteiro
            id_cliente = int(id_cliente)
            
            # Verifica se o valor é positivo (IDs devem ser maiores que zero)
            if id_cliente <= 0:
                erros.append("O 'id_cliente' deve ser positivo.")
        
        # Captura erros se a conversão para inteiro falhar
        except (ValueError, TypeError):
            erros.append("O 'id_cliente' deve ser um número inteiro.")

    # Se houver erros de validação de tipos, retorna antes de sanitizar
    if erros:
        return None, erros

    # --- ETAPA 4: Sanitização (Limpeza e Padronização) ---
    # Cria um dicionário limpo com os dados validados e padronizados
    pedido_limpo = {
        "id_cliente": id_cliente,  # ID do cliente (já validado)
        "data": dados_brutos['data'],  # Data do agendamento
        "horario": dados_brutos['horario'],  # Horário do agendamento
        "id_barbeiro": dados_brutos.get('id_barbeiro', 1),  # ID do barbeiro (padrão: 1)
        "id_servico": dados_brutos.get('id_servico', 1)  # ID do serviço (padrão: 1)
    }
    
    # --- ETAPA 5: Retorno Bem-Sucedido ---
    # Retorna os dados limpos e None para erros (indicando sucesso)
    return pedido_limpo, None