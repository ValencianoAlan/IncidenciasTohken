from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user_model import UserModel

# Crear un Blueprint para las rutas de usuario
user_bp = Blueprint('user', __name__)
user_model = UserModel()

# Ruta para agregar usuario
@user_bp.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    # Verificar si el usuario tiene permisos de administrador
    if 'rol' not in session or session['rol'] != 'Admin':
        flash("No tienes permiso para acceder a esta página", "error")
        return redirect(url_for('auth.bienvenida'))

    mensaje = None
    roles = user_model.get_roles()  # Obtener la lista de roles desde el modelo

    if request.method == 'POST':
        # Obtener datos del formulario
        numNomina = request.form.get('numNomina')
        nombre = request.form.get('nombre')
        apellido_paterno = request.form.get('apellidoPaterno', '')
        apellido_materno = request.form.get('apellidoMaterno', '')
        username = request.form.get('username')
        password = request.form.get('password')
        idRol = request.form.get('idRol')

        # Validar campos obligatorios
        if numNomina and nombre and username and password and idRol:
            if user_model.add_user(numNomina, nombre, apellido_paterno, apellido_materno, username, password, idRol):
                mensaje = "Usuario agregado exitosamente."
            else:
                mensaje = "Error al agregar usuario."
        else:
            mensaje = "Por favor, completa todos los campos obligatorios."

    return render_template('agregar_usuario.html', mensaje=mensaje, roles=roles)

# Ruta para ver registros de usuarios
@user_bp.route('/ver_registros', methods=['GET', 'POST'])
def ver_registros():
    # Verificar si el usuario está autenticado
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    busqueda = request.form.get('numNomina') if request.method == 'POST' else None
    registros = user_model.get_all_users()  # Obtener todos los usuarios

    # Filtrar por número de nómina si se proporciona una búsqueda
    if busqueda:
        usuario = user_model.get_user_by_numNomina(busqueda)
        registros = [usuario] if usuario else []

    return render_template('ver_registros.html', registros=registros, busqueda=busqueda, username=session['user'])

@user_bp.route('/borrar_usuario/<int:numNomina>', methods=['POST'])
def borrar_usuario(numNomina):
    if 'rol' not in session or session['rol'] != 'Admin':
        flash("No tienes permiso para realizar esta acción", "error")
        return redirect(url_for('auth.bienvenida'))

    if user_model.delete_user(numNomina):
        flash("Usuario borrado exitosamente", "success")
    else:
        flash("Error al borrar usuario", "error")

    return redirect(url_for('user.ver_registros'))

@user_bp.route('/editar_usuario/<int:numNomina>', methods=['GET', 'POST'])
def editar_usuario(numNomina):
    if 'rol' not in session or session['rol'] != 'Admin':
        flash("No tienes permiso para acceder a esta página", "error")
        return redirect(url_for('auth.bienvenida'))

    usuario = user_model.get_user_by_numNomina(numNomina)
    roles = user_model.get_roles()

    if not usuario:
        return "Usuario no encontrado", 404

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellidoPaterno']
        apellido_materno = request.form['apellidoMaterno']
        username = request.form['username']
        idRol = request.form['idRol']

        if user_model.update_user(numNomina, nombre, apellido_paterno, apellido_materno, username, idRol):
            flash("Usuario actualizado exitosamente", "success")
            return redirect(url_for('user.ver_registros'))
        else:
            flash("Error al actualizar usuario", "error")

    return render_template('editar_usuario.html', usuario=usuario, roles=roles, username=session['user'])