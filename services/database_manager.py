# database_manager.py
from ast import expr_context
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
        
# Em services/database_manager.py

def editar_agendamento(id_agendamento, novos_dados, id_autor, tipo_autor):
    conn = get_db_connection()
    # Define qual coluna será usada na trava de segurança
    coluna_trava = "id_barbeiro" if tipo_autor == "barbeiro" else "id_cliente"
    
    try:
        query = f'''
            UPDATE agendamentos 
            SET data = ?, horario = ?, id_barbeiro = ?, id_servico = ? 
            WHERE id = ? AND {coluna_trava} = ? AND confirmado = 0
        '''
        cursor = conn.execute(query, (
            novos_dados['data'], novos_dados['horario'], 
            novos_dados['id_barbeiro'], novos_dados['id_servico'],
            id_agendamento, id_autor
        ))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro no banco: {e}")
        return False
    finally:
        conn.close()

# Em services/database_manager.py

def deletar_agendamento(id_agendamento, id_autor, tipo_autor):
    conn = get_db_connection()
    # Define a trava baseada em quem está deletando
    coluna_trava = "id_barbeiro" if tipo_autor == "barbeiro" else "id_cliente"
    
    try:
        # SQL Parametrizado: ID + Dono + Segurança de Status
        sql = f'DELETE FROM agendamentos WHERE id = ? AND {coluna_trava} = ? AND confirmado = 0'
        cursor = conn.execute(sql, (id_agendamento, id_autor))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao deletar: {e}")
        return False
    finally:
        conn.close()
    
def confirmar_agendamento(id_agendamento, id_barbeiro):
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            f"UPDATE agendamentos SET confirmado = 1 WHERE id = ? AND id_barbeiro = ? AND confirmado = 0",
            (id_agendamento, id_barbeiro)
        )
        conn.commit()
        if cursor.rowcount == 0:
           return False
       
        return True 
    except Exception as e:
        print(f"Erro ao confirmar agendamento - {e}")
        return False
    finally:
        conn.close()

# --- GESTÃO DE CLIENTES ---

def verificar_existencia_cliente(cpf, email):
    """
    Verifica se já existe algum cliente com o mesmo CPF ou E-mail.
    Retorna: "cpf", "email" ou None (se estiver livre).
    """
    conn = get_db_connection()
    try:
        # Verifica CPF
        cursor = conn.execute('SELECT id FROM clientes WHERE num_documento = ?', (cpf,))
        if cursor.fetchone():
            return "cpf"
        
        # Verifica E-mail
        cursor = conn.execute('SELECT id FROM clientes WHERE email = ?', (email,))
        if cursor.fetchone():
            return "email"
            
        return None
    finally:
        conn.close()

def inserir_cliente(dados):
    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO clientes (nome_cliente, data_registro, tipo_documento, num_documento, telefone, email)
            VALUES (?, date('now'), 'CPF', ?, ?, ?)
        """, (dados['nome'], dados['cpf'], dados['telefone'], dados['email']))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao inserir cliente: {e}")
        return False
    finally:
        conn.close()
                