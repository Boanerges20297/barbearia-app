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
            cliente_nome TEXT NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            id_barbeiro INTEGER,
            id_servico INTEGER
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

def inserir_agendamento(cliente_nome, data, horario, id_barbeiro, id_servico):
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO agendamentos (cliente_nome, data, horario, id_barbeiro, id_servico) VALUES (?, ?, ?, ?, ?)',
            (cliente_nome, data, horario, id_barbeiro, id_servico)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
        return False
    finally:
        conn.close()