from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user_model import UserModel
from flask import jsonify

# Crear un Blueprint para las rutas de usuario
user_bp = Blueprint('user', __name__)
user_model = UserModel()

# Ruta para agregar usuario
@user_bp.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    # Solo el Admin puede agregar usuarios
    if 'rol' not in session or session['rol'] != 'Admin':
        flash("No tienes permiso para acceder a esta página", "error")
        return redirect(url_for('auth.bienvenida'))

    mensaje = None
    departamentos = user_model.get_departamentos()  # Obtener departamentos
    roles = user_model.get_roles()  # Obtener roles

    if request.method == 'POST':
        numNomina = request.form.get('numNomina')
        nombre = request.form.get('nombre')
        apellido_paterno = request.form.get('apellidoPaterno', '')
        apellido_materno = request.form.get('apellidoMaterno', '')
        username = request.form.get('username')
        password = request.form.get('password')
        idRol = request.form.get('idRol')
        idDepartamento = request.form.get('idDepartamento')  # Obtener el departamento
        idPuesto = request.form.get('idPuesto')  # Obtener el puesto

        if numNomina and nombre and username and password and idRol and idDepartamento and idPuesto:
            if user_model.add_user(numNomina, nombre, apellido_paterno, apellido_materno, username, password, idRol, idDepartamento, idPuesto):
                flash("Usuario agregado exitosamente", "success")
                return redirect(url_for('auth.bienvenida'))
            else:
                flash("Error al agregar usuario", "error")
        else:
            flash("Por favor, completa todos los campos obligatorios", "error")

    return render_template('agregar_usuario.html', mensaje=mensaje, departamentos=departamentos, roles=roles)

@user_bp.route('/ver_registros', methods=['GET', 'POST'])
def ver_registros():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    busqueda = request.form.get('numNomina') if request.method == 'POST' else None
    registros = user_model.get_all_users_with_details()  # Obtener todos los usuarios con detalles

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

    return redirect(url_for('auth.bienvenida'))

@user_bp.route('/editar_usuario/<int:numNomina>', methods=['GET', 'POST'])
def editar_usuario(numNomina):
    if 'rol' not in session or session['rol'] not in ['Admin', 'Supervisor', 'Gerente']:
        flash("No tienes permiso para acceder a esta página", "error")
        return redirect(url_for('auth.bienvenida'))

    # Obtener el usuario que se va a editar
    usuario = user_model.get_user_by_numNomina(numNomina)
    departamentos = user_model.get_departamentos()  # Obtener departamentos
    puestos = user_model.get_puestos();
    roles = user_model.get_roles()  # Obtener roles

    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('auth.bienvenida'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellidoPaterno']
        apellido_materno = request.form['apellidoMaterno']
        username = request.form['username']
        idDepartamento = request.form['idDepartamento']  # Obtener el departamento
        idPuesto = request.form['idPuesto']  # Obtener el puesto
        idRol = request.form['idRol']  # Obtener el rol

        if user_model.update_user(numNomina, nombre, apellido_paterno, apellido_materno, username, idDepartamento, idPuesto, idRol):
            flash("Usuario actualizado exitosamente", "success")
            return redirect(url_for('user.ver_registros'))
        else:
            flash("Error al actualizar usuario", "error")

    return render_template('editar_usuario.html', usuario=usuario, departamentos=departamentos, puestos=puestos,roles=roles, username=session['user'])

@user_bp.route('/obtener_puestos_por_departamento/<int:idDepartamento>', methods=['GET'])
def obtener_puestos_por_departamento(idDepartamento):
    puestos = user_model.get_puestos_por_departamento(idDepartamento)
    return jsonify(puestos)

@user_bp.route('/incidencias_usuario')
def incidencias_usuario():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Obtener todos los usuarios con detalles
    registros = user_model.get_all_users_with_details()

    return render_template('incidencias_usuario.html', registros=registros, username=session['user'])
