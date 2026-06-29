import os
from flask import Flask, redirect, url_for
from config import Config

# Importar controladores
from controllers.usuario_controller import usuario_bp
from controllers.jefe_controller import jefe_bp
from controllers.auth_controller import auth_bp # <--- IMPORTANTE

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'tu_clave_secreta_aqui'

# Registrar Blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(jefe_bp)
app.register_blueprint(auth_bp) # <--- IMPORTANTE

app.config["MAIL_SERVER"] = "smtp.gmail.com"   # Servidor de Gmail [cite: 2888]
app.config["MAIL_PORT"] = 587                  # Puerto seguro [cite: 2889]
app.config["MAIL_USE_TLS"] = True              # Conexión cifrada [cite: 2890]
app.config["MAIL_USERNAME"] = "soporte@tohken.mx"        # Tu correo corporativo [cite: 2891]
app.config["MAIL_PASSWORD"] = "rhfd pdgy njmh dhag"          # Contraseña de aplicación

# Ahora la raíz de tu web redirige directamente al Login
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)