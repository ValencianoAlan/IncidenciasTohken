from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user_model import UserModel

# Crear un Blueprint
user_bp = Blueprint('user', __name__)
user_model = UserModel()

@user_bp.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    mensaje = None
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido_paterno = request.form.get('apellidoPaterno')
        apellido_materno = request.form.get('apellidoMaterno')
        username = request.form.get('username')
        password = request.form.get('password')
        if nombre and apellido_paterno and apellido_materno and username and password:
            if user_model.add_user(nombre, apellido_paterno, apellido_materno, username, password):
                mensaje = "Usuario agregado exitosamente."
            else:
                mensaje = "Error al agregar usuario."
        else:
            mensaje = "Por favor, completa todos los campos."
    return render_template('agregar_usuario.html', mensaje=mensaje)

@user_bp.route('/ver_registros', methods=['GET', 'POST'])
def ver_registros():
    registros = []
    busqueda = None
    if request.method == 'POST':
        busqueda = request.form.get('idUsuario')
        if busqueda:
            usuario = user_model.get_user_by_id(busqueda)
            if usuario:
                registros = [usuario]
        else:
            registros = user_model.get_all_users()
    else:
        registros = user_model.get_all_users()
    return render_template('ver_registros.html', registros=registros, busqueda=busqueda, username=session['user'])

@user_bp.route('/borrar_usuario/<int:id>', methods=['POST'])
def borrar_usuario(id):
    if user_model.delete_user(id):
        flash("Usuario borrado exitosamente", "success")
    else:
        flash("Error al borrar usuario", "error")
    return redirect(url_for('user.ver_registros'))

@user_bp.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = user_model.get_user_by_id(id)
    if not usuario:
        return "Usuario no encontrado", 404
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellidoPaterno']
        apellido_materno = request.form['apellidoMaterno']
        username = request.form['username']
        if user_model.update_user(id, nombre, apellido_paterno, apellido_materno, username):
            if id == session['user_id']:
                session['user'] = f"{nombre} {apellido_paterno} {apellido_materno}"
            return redirect(url_for('user.ver_registros'))
    return render_template('editar_usuario.html', usuario=usuario, username=session['user'])