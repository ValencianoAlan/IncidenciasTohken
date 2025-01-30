from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user_model import UserModel

# Crear un Blueprint en lugar de una app Flask
auth_bp = Blueprint('auth', __name__, template_folder="views/templates")
user_model = UserModel()

@auth_bp.route('/')
def login():
    return render_template('login.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def do_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = user_model.authenticate_user(username, password)
        if usuario:
            session['user_id'] = usuario.idUsuario
            session['user'] = f"{usuario.nombre} {usuario.apellidoPaterno} {usuario.apellidoMaterno}"
            return redirect(url_for('auth.bienvenida'))
        else:
            flash("Usuario o contraseña incorrectos", "error")
            return redirect(url_for('auth.do_login'))
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

@auth_bp.route("/enviar_correo", methods=["POST"])
def enviar_correo():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    # Obtener datos del formulario
    destinatario = request.form.get("destinatario")
    asunto = request.form.get("asunto")
    cuerpo = request.form.get("cuerpo")

    # Enviar correo
    if user_model.enviar_correo(destinatario, asunto, cuerpo):
        flash("Correo enviado exitosamente", "success")
    else:
        flash("Error al enviar el correo", "error")

    return redirect(url_for("auth.bienvenida"))