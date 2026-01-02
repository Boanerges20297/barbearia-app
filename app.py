# app.py
from flask import Flask, render_template
from routes import confirmar_agendamento
from routes.deletar_agendamento import deletar_agendamento_bp
from routes.confirmar_agendamento import confirmar_agendamento_bp
from routes.editar_agendamento import editar_agendamento_bp
from routes.agendamentos_routes import agendamento_bp
from services.database_manager import init_db

app = Flask(__name__)

# --- SEGURANÇA ---
# Isso é necessário para usar sessões (cookies seguros)
app.secret_key = 'sua_chave_super_secreta_aqui' 

# --- INICIALIZAÇÃO METODOLÓGICA ---
init_db() # O banco é preparado aqui, uma única vez!

app.register_blueprint(agendamento_bp)
app.register_blueprint(editar_agendamento_bp)
app.register_blueprint(deletar_agendamento_bp)
app.register_blueprint(confirmar_agendamento_bp)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)