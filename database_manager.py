# database_manager.py
import sqlite3

DB_NAME = 'barbearia.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Cria o esquema do banco de dados. 
    Deve ser chamada na inicialização do App.
    """
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            id_barbeiro INTEGER,
            id_servico INTEGER,
            confirmado BOOLEAN DEFAULT 0
        );
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT NOT NULL,
            data_registro TEXT NOT NULL,
            tipo_documento TEXT NOT NULL,
            num_documento TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL
        );
    """)
    
    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado com sucesso.")

def ler_todos_agendamentos():
    conn = get_db_connection()
    # Note como a função agora foca apenas em sua responsabilidade: LER
    agendamentos = conn.execute('SELECT * FROM agendamentos').fetchall()
    conn.close()
    # Abaixo retornamos uma lista de dicionários para facilitar o uso dos dados
    return [dict(row) for row in agendamentos]

def inserir_agendamento(id_cliente, data, horario, id_barbeiro, id_servico):
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO agendamentos (id_cliente, data, horario, id_barbeiro, id_servico) VALUES (?, ?, ?, ?, ?)',
            (id_cliente, data, horario, id_barbeiro, id_servico)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
        return False
    finally:
        conn.close()
        
def editar_agendamento(id_agendamento, novos_dados):
    conn = get_db_connection()
    # Verificar se novos_dados contém as chaves necessárias
    if not all (k in novos_dados for k in ("data", "horario", "id_barbeiro", "id_servico")):
        raise ValueError("novos_dados deve conter 'data', 'horario', 'id_barbeiro' e 'id_servico'")
    
    try:
        conn.execute(
            'UPDATE agendamentos SET data = ?, horario = ?, id_barbeiro = ?, id_servico = ? WHERE id = ? AND confirmado = 0',
            (novos_dados['data'], novos_dados['horario'], novos_dados['id_barbeiro'], novos_dados['id_servico'], id_agendamento)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao editar no banco: {e}")
        return False
    finally:
        conn.close()

def deletar_agendamento(id_agendamento):
    conn = get_db_connection()
    try:
        conn.execute(
            'DELETE FROM agendamentos WHERE id = ? AND confirmado = 0',
            (id_agendamento,)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao deletar no banco: {e}")
        return False
    finally:
        conn.close()