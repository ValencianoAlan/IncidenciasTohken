import os
from flask import Flask, redirect, url_for
from config import Config

# Importar controladores
from controllers.usuario_controller import usuario_bp
from controllers.jefe_controller import jefe_bp
from controllers.auth_controller import auth_bp # <--- IMPORTANTE

app = Flask(__name__)
app.config.from_object(Config)

# Registrar Blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(jefe_bp)
app.register_blueprint(auth_bp) # <--- IMPORTANTE

# Ahora la raíz de tu web redirige directamente al Login
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)