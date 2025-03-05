from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.models.user_model import UserModel

incidencias_bp = Blueprint('incidencias', __name__)
user_model = UserModel()

@incidencias_bp.route('/ver_incidencias')
def ver_incidencias():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Obtener puestos y departamentos desde la base de datos
    puestos = user_model.get_puestos()
    departamentos = user_model.get_departamentos()

    # Obtener los días de vacaciones restantes del usuario actual
    vacaciones = user_model.get_vacaciones(session['numNomina'])

    return render_template('incidencia.html', puestos=puestos, departamentos=departamentos, vacaciones=vacaciones)

@incidencias_bp.route('/crear_incidencia_usuario/<int:numNomina>/<origen>', methods=['GET', 'POST'])
def crear_incidencia_usuario(numNomina, origen):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Obtener los datos del usuario
    usuario = user_model.get_user_by_numNomina(numNomina)
    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('auth.bienvenida'))

    # Obtener la fecha actual
    from datetime import datetime
    fecha_solicitud = datetime.now().strftime('%Y-%m-%d')

    # Obtener el nombre del departamento y puesto del usuario
    departamento_usuario = user_model.get_departamento_by_id(usuario['idDepartamento'])
    puesto_usuario = user_model.get_puesto_by_id(usuario['idPuesto'])

    # Obtener todos los puestos y departamentos para los selectores
    puestos = user_model.get_puestos()
    departamentos = user_model.get_departamentos()

    return render_template('incidencia.html', 
                           nombre=usuario['nombre'],
                           apellido_paterno=usuario['apellidoPaterno'],
                           apellido_materno=usuario['apellidoMaterno'],
                           fecha_solicitud=fecha_solicitud,
                           puesto=usuario['idPuesto'],
                           nombre_puesto=puesto_usuario['nombrePuesto'],  # Acceder al valor usando la clave
                           no_nomina=usuario['numNomina'],
                           departamento=usuario['idDepartamento'],
                           nombre_departamento=departamento_usuario['nombreDepartamento'],  # Acceder al valor usando la clave
                           dias_vacaciones=usuario['diasVacaciones'],  # Días de vacaciones
                           puestos=puestos,
                           departamentos=departamentos,
                           origen=origen)  # Pasamos el origen a la plantilla