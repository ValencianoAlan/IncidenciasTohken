from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.models.user_model import UserModel

incidencias_bp = Blueprint('incidencias', __name__)
user_model = UserModel()

@incidencias_bp.route('/procesar_incidencia/<int:idIncidencia>', methods=['POST'])
def procesar_incidencia(idIncidencia):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Obtener la incidencia por su ID
    incidencia = user_model.get_incidencia_by_id(idIncidencia)

    if not incidencia:
        flash("Incidencia no encontrada", "error")
        return redirect(url_for('incidencias.solicitudes_recibidas'))

    # Verificar si la incidencia ya ha sido aprobada o rechazada
    if incidencia['estatus'] in ['Aprobada', 'Rechazada']:
        flash("No se puede modificar el estado de una incidencia ya procesada", "error")
        return redirect(url_for('incidencias.solicitudes_recibidas'))

    accion = request.form.get('accion')  # 'aprobar' o 'rechazar'
    if accion == 'aprobar':
        user_model.actualizar_estatus_incidencia(idIncidencia, 'Aprobada')
        flash("Incidencia aprobada correctamente", "success")
    elif accion == 'rechazar':
        user_model.actualizar_estatus_incidencia(idIncidencia, 'Rechazada')
        flash("Incidencia rechazada correctamente", "success")

    return redirect(url_for('incidencias.solicitudes_recibidas'))

@incidencias_bp.route('/crear_incidencia', methods=['GET', 'POST'])
def crear_incidencia():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Obtener los datos del formulario
        numNomina_solicitante = session['numNomina']
        nombre_solicitante = request.form.get('nombre')
        apellido_paterno = request.form.get('apellido_paterno')
        apellido_materno = request.form.get('apellido_materno')
        fecha_solicitud = request.form.get('fecha_solicitud')
        puesto = request.form.get('puesto')
        departamento = request.form.get('departamento')
        dias_vacaciones = request.form.get('dias_vacaciones')
        motivo = request.form.get('motivo')
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        num_dias = request.form.get('num_dias')
        observaciones = request.form.get('comentarios')

        # Obtener el jefe directo del usuario
        jefe_directo = user_model.get_jefe_directo(numNomina_solicitante)

        # Guardar la incidencia en la base de datos
        idIncidencia = user_model.crear_incidencia(
            numNomina_solicitante,
            nombre_solicitante,
            apellido_paterno,
            apellido_materno,
            fecha_solicitud,
            puesto,
            departamento,
            dias_vacaciones,
            motivo,
            fecha_inicio,
            fecha_fin,
            num_dias,
            observaciones,
            jefe_directo
        )

        if idIncidencia:
            return redirect(url_for('incidencias.mis_solicitudes'))
        else:
            flash("Error al enviar la solicitud", "error")

    return render_template('incidencia.html')


@incidencias_bp.route('/ver_incidencia/<int:idIncidencia>/<origen>', methods=['GET'])
def ver_incidencia(idIncidencia, origen):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Obtener la incidencia
    incidencia = user_model.get_incidencia_by_id(idIncidencia)

    if not incidencia:
        flash("Incidencia no encontrada", "error")
        return redirect(url_for('incidencias.solicitudes_recibidas'))

    if request.method == 'POST':
        accion = request.form.get('accion')  # 'aprobar' o 'rechazar'
        if accion == 'aprobar':
            user_model.actualizar_estatus_incidencia(idIncidencia, 'Aprobada')
            # Enviar correo al usuario
            user_model.enviar_correo_incidencia(incidencia.numNomina_solicitante, 'Aprobada')
        elif accion == 'rechazar':
            user_model.actualizar_estatus_incidencia(idIncidencia, 'Rechazada')
            # Enviar correo al usuario
            user_model.enviar_correo_incidencia(incidencia.numNomina_solicitante, 'Rechazada')

        return redirect(url_for('incidencias.solicitudes_recibidas'))

    return render_template('ver_incidencia.html', incidencia=incidencia, origen=origen)

@incidencias_bp.route('/solicitudes_recibidas')
def solicitudes_recibidas():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Obtener el parámetro de orden (ascendente o descendente)
    orden = request.args.get('orden', 'asc')  # Por defecto, orden ascendente

    # Obtener las solicitudes recibidas por el jefe directo
    numNomina_jefe = session['numNomina']
    solicitudes = user_model.get_solicitudes_recibidas(numNomina_jefe, orden)

    return render_template('solicitudes_recibidas.html', solicitudes=solicitudes, orden=orden)

@incidencias_bp.route('/mis_solicitudes')
def mis_solicitudes():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Obtener el parámetro de orden (ascendente o descendente)
    orden = request.args.get('orden', 'asc')  # Por defecto, orden ascendente

    # Obtener las solicitudes enviadas por el usuario actual
    numNomina = session['numNomina']
    solicitudes = user_model.get_solicitudes_enviadas(numNomina, orden)

    return render_template('mis_solicitudes.html', solicitudes=solicitudes, orden=orden)

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
