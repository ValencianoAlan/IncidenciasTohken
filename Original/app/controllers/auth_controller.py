from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user_model import UserModel
import re

# Crear un Blueprint en lugar de una app Flask
auth_bp = Blueprint('auth', __name__, template_folder="views/templates")
user_model = UserModel()

@auth_bp.route('/')
def login():
    return render_template('login.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def do_login():
    if request.method == 'POST':
        login_input = request.form['login_input']
        password = request.form['password']
        
        resultado = user_model.authenticate_user(login_input, password)
        
        if resultado["success"]:
            usuario = resultado["data"]
            session['numNomina'] = usuario.numNomina
            session['user'] = f"{usuario.nombre} {usuario.apellidoPaterno} {usuario.apellidoMaterno}"
            session['rol'] = usuario.nombreRol
            return redirect(url_for('auth.bienvenida'))
        else:
            # En la sección de flash:
            if resultado["error"] == "user_not_found":
                flash("Usuario o número de nómina no registrado", "user_not_found")
            elif resultado["error"] == "wrong_password":
                flash("Contraseña incorrecta", "wrong_password")
            else:
                flash("Error en el servidor. Intente nuevamente", "error")
                
    return render_template('login.html')

@auth_bp.route('/bienvenida')
def bienvenida():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('bienvenida.html', username=session['user'])

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))

# Función de validación (agrégala al inicio del archivo)
def es_correo_valido(correo):
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(patron, correo) is not None

# ... (otras rutas y código existente)

@auth_bp.route("/enviar_correo", methods=["POST"])
def enviar_correo():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    # Obtener y procesar correos
    destinatarios_raw = request.form.get("destinatario", "")
    destinatarios = [email.strip() for email in destinatarios_raw.split(",") if email.strip()]

    # Validar correos
    correos_invalidos = [email for email in destinatarios if not es_correo_valido(email)]
    
    if correos_invalidos:
        flash(f"Correos inválidos: {', '.join(correos_invalidos)}", "error")
        return redirect(url_for("auth.bienvenida"))

    if not destinatarios:
        flash("Debes ingresar al menos un correo válido", "error")
        return redirect(url_for("auth.bienvenida"))

    # Obtener asunto y cuerpo
    asunto = request.form.get("asunto", "")
    cuerpo = request.form.get("cuerpo", "")

    # Enviar correo
    if user_model.enviar_correo(destinatarios, asunto, cuerpo):
        flash(f"Correo enviado exitosamente a {len(destinatarios)} destinatarios", "success")
    else:
        flash("Error al enviar el correo", "error")

    return redirect(url_for("auth.bienvenida"))