from flask import session
from app import create_app
from datetime import datetime


app = create_app()

from app.models.user_model import UserModel
user_model = UserModel()

# Registrar la función en Jinja2
@app.context_processor
def utility_processor():
    return {
        'obtener_nombre_usuario': user_model.obtener_nombre_usuario,
        'current_user_rol': lambda: session.get('rol', None)  # Función adicional útil
    }

@app.template_filter('format_datetime')
def format_datetime_filter(value, format="%d/%m/%Y %H:%M"):
    if value is None:
        return ""
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return value.strftime(format)

if __name__ == '__main__':
    app.run(debug=True)