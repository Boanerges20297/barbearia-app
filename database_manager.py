# database_manager.py
import sqlite3

DB_NAME = 'barbearia.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def ler_todos_agendamentos():
    conn = get_db_connection()
    
    # --- BLINDAGEM: Cria a tabela se ela não existir ---
    # Isso impede o erro "no such table" se você deletar o arquivo .db
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
    # ---------------------------------------------------

    agendamentos = conn.execute('SELECT * FROM agendamentos').fetchall()
    conn.close()
    return [dict(row) for row in agendamentos]

def inserir_agendamento(cliente_nome, data, horario, id_barbeiro, id_servico):
    conn = get_db_connection()
    try:
        # Garante que a tabela existe antes de tentar inserir também
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