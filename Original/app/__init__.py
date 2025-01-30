from flask import Flask
from app.controllers.auth_controller import auth_bp
from app.controllers.user_controller import user_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="views/templates",  # ¡Ruta personalizada!
        static_folder="views/static"        # Ruta para archivos estáticos
    )
    app.secret_key = "tu_clave_secreta"
    
    app.config["MAIL_SERVER"] = "smtp.gmail.com"  # Ejemplo para Gmail
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "escaner.ttm@tohken.mx"
    app.config["MAIL_PASSWORD"] = "Tohken2025"  # No la expongas públicamente

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    return app
