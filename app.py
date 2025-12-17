# app.py
from flask import Flask, render_template
from routes.agendamentos_routes import agendamento_bp

app = Flask(__name__)

# --- SEGURANÇA ---
# Isso é necessário para usar sessões (cookies seguros)
app.secret_key = 'sua_chave_super_secreta_aqui' 

app.register_blueprint(agendamento_bp)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)