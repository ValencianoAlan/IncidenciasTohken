from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.models.user_model import UserModel

incidencias_bp = Blueprint('incidencias', __name__)
user_model = UserModel()

@incidencias_bp.route('/procesar_incidencia/<int:idIncidencia>', methods=['POST'])
def procesar_incidencia(idIncidencia):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    incidencia = user_model.get_incidencia_by_id(idIncidencia)
    if not incidencia:
        flash("Incidencia no encontrada", "error")
        return redirect(url_for('incidencias.solicitudes_recibidas'))
    
    if incidencia['estatus'] in ['Aprobada', 'Rechazada']:
        flash("Esta incidencia ya ha sido procesada y no puede modificarse", "error")
        return redirect(url_for('incidencias.solicitudes_recibidas'))

    if 'jefe_directo' not in incidencia:
        flash("Error en los datos de la incidencia", "error")
        return redirect(url_for('incidencias.solicitudes_recibidas'))

    current_user_nomina = session['numNomina']
    accion = request.form.get('accion')
    comentarios = request.form.get('comentarios', '')

        # Verificar si ya está aprobada/rechazada
    if incidencia['estatus'] in ['Aprobada', 'Rechazada']:
        flash("Esta incidencia ya ha sido procesada y no puede modificarse", "warning")
        return redirect(url_for('incidencias.solicitudes_recibidas'))

    if incidencia['estatus'] == 'Pendiente Supervisor':
        if current_user_nomina != incidencia['jefe_directo']:
            flash("No tienes permiso para procesar esta incidencia", "error")
            return redirect(url_for('incidencias.solicitudes_recibidas'))

        if accion == 'aprobar':
            if not user_model.actualizar_estatus_incidencia(
                idIncidencia, 
                'Pendiente Gerente',
                current_user_nomina,
                comentarios
            ):
                flash("Error al actualizar el estado", "error")
                return redirect(url_for('incidencias.solicitudes_recibidas'))
            
            # Cuando el supervisor aprueba y envía al usuario
            user_model.enviar_notificacion_incidencia(
                incidencia['numNomina_solicitante'],
                'Aprobada',
                incidencia['motivo'],
                incidencia['fecha_inicio'],
                incidencia['fecha_fin'],
                aprobador_rol='supervisor'
            )
            
            # Cuando el supervisor aprueba y envía al gerente
            user_model.enviar_notificacion_incidencia(
                incidencia['numNomina_solicitante'],
                'Nueva solicitud para revisión',
                incidencia['motivo'],
                incidencia['fecha_inicio'],
                incidencia['fecha_fin'],
                incidencia['gerente_responsable']
            )

            # Obtener correo del gerente (jefe del supervisor)
            gerente = user_model.get_user_by_numNomina(incidencia['gerente_responsable'])
            if not gerente:
                flash("No se encontró al gerente responsable", "error")
                return redirect(url_for('incidencias.solicitudes_recibidas'))
            
            solicitante = user_model.get_user_by_numNomina(incidencia['numNomina_solicitante'])


            # 4. Enviar notificación al gerente
            if not user_model.enviar_notificacion_gerente(
                incidencia_id=idIncidencia,
                gerente_nomina=incidencia['gerente_responsable'],
                solicitante_nombre=f"{solicitante['nombre']} {solicitante['apellidoPaterno']}",
                supervisor_nombre=session['user'],
                motivo=incidencia['motivo'],
                fecha_inicio=incidencia['fecha_inicio'],
                fecha_fin=incidencia['fecha_fin'],
                comentarios=comentarios
            ):
                flash("Incidencia aprobada pero no se pudo notificar al gerente", "warning")
            else:
                flash("Incidencia aprobada y gerente notificado", "success")
            
            # Notificar al EMPLEADO que su solicitud avanzó
            # Cuando se notifica al usuario
            user_model.enviar_notificacion_incidencia(
                incidencia['numNomina_solicitante'],
                'Aprobada por supervisor - Pendiente de gerente',
                incidencia['motivo'],
                incidencia['fecha_inicio'],
                incidencia['fecha_fin'],
                None,  # destinatario (None = usuario solicitante)
                f"Tu solicitud ha sido aprobada por tu supervisor y está pendiente de aprobación por el gerente. Comentarios: {comentarios}"
            )
            
            flash("Incidencia aprobada por supervisor y enviada a gerente", "success")
            
        elif accion == 'rechazar':
            # Cambiar estado directamente a Rechazada (sin pasar por gerente)
            if not user_model.actualizar_estatus_incidencia(
                idIncidencia, 
                'Rechazada',
                current_user_nomina,
                comentarios
            ):
                flash("Error al actualizar la incidencia", "error")
                return redirect(url_for('incidencias.solicitudes_recibidas'))

            # Notificar solo al usuario solicitante
            user_model.enviar_notificacion_incidencia(
                incidencia['numNomina_solicitante'],
                'Rechazada por tu supervisor',
                incidencia['motivo'],
                incidencia['fecha_inicio'],
                incidencia['fecha_fin']
            )
            
            flash("Incidencia rechazada por supervisor", "success")

    elif incidencia['estatus'] == 'Pendiente Gerente':
        # Solo el gerente puede aprobar en esta etapa
        if current_user_nomina != incidencia['gerente_responsable']:
            flash("No tienes permiso para procesar esta incidencia", "error")
            return redirect(url_for('incidencias.solicitudes_recibidas'))
            
        if accion == 'aprobar':
            if not user_model.actualizar_estatus_incidencia(
                idIncidencia,
                'Aprobada',
                current_user_nomina,
                comentarios
            ):
                flash("Error al actualizar el estado", "error")
                return redirect(url_for('incidencias.solicitudes_recibidas'))
            
            # Notificar al usuario
            user_model.enviar_notificacion_incidencia(
                incidencia['numNomina_solicitante'],
                'Aprobada',
                incidencia['motivo'],
                incidencia['fecha_inicio'],
                incidencia['fecha_fin'],
                aprobador_rol='gerente'
            )
            
            flash("Incidencia aprobada por gerente", "success")
            
        elif accion == 'rechazar':
            user_model.actualizar_estatus_incidencia(
                idIncidencia,
                'Rechazada',
                current_user_nomina,
                comentarios
            )
            
            # Notificar al usuario
            user_model.enviar_notificacion_incidencia(
                incidencia['numNomina_solicitante'],
                'Rechazada',
                incidencia['motivo'],
                incidencia['fecha_inicio'],
                incidencia['fecha_fin'],
                aprobador_rol='gerente'
            )
            
            flash("Incidencia rechazada por gerente", "success")
    
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

@incidencias_bp.route('/solicitudes_recibidas', methods=['GET', 'POST'])
def solicitudes_recibidas():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
        
    numNomina_jefe = session['numNomina']
    motivos = user_model.get_motivos_incidencias()
    
    # Procesar filtros
    filtros = {}
    if request.method == 'POST':
        filtros['estado'] = request.form.get('estado')
        filtros['fecha_desde'] = request.form.get('fecha_desde')
        filtros['fecha_hasta'] = request.form.get('fecha_hasta')
        filtros['id_incidencia'] = request.form.get('id_incidencia')
        filtros['motivo'] = request.form.get('motivo')
    else:
        filtros['estado'] = request.args.get('estado')
        filtros['fecha_desde'] = request.args.get('fecha_desde')
        filtros['fecha_hasta'] = request.args.get('fecha_hasta')
        filtros['id_incidencia'] = request.args.get('id_incidencia')
        filtros['motivo'] = request.args.get('motivo')
    
    solicitudes = user_model.get_solicitudes_recibidas_filtradas(numNomina_jefe, filtros)
    
    return render_template('solicitudes_recibidas.html',
                         solicitudes=solicitudes,
                         motivos=motivos,
                         filtros=filtros)

@incidencias_bp.route('/mis_solicitudes', methods=['GET', 'POST'])
def mis_solicitudes():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
        
    numNomina = session['numNomina']
    motivos = user_model.get_motivos_incidencias()
    
    # Procesar filtros
    filtros = {}
    if request.method == 'POST':
        filtros['estado'] = request.form.get('estado')
        filtros['fecha_desde'] = request.form.get('fecha_desde')
        filtros['fecha_hasta'] = request.form.get('fecha_hasta')
        filtros['id_incidencia'] = request.form.get('id_incidencia')
        filtros['motivo'] = request.form.get('motivo')
    else:
        filtros['estado'] = request.args.get('estado')
        filtros['fecha_desde'] = request.args.get('fecha_desde')
        filtros['fecha_hasta'] = request.args.get('fecha_hasta')
        filtros['id_incidencia'] = request.args.get('id_incidencia')
        filtros['motivo'] = request.args.get('motivo')
    
    solicitudes = user_model.get_solicitudes_enviadas_filtradas(numNomina, filtros)
    
    return render_template('mis_solicitudes.html',
                         solicitudes=solicitudes,
                         motivos=motivos,
                         filtros=filtros)

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

@incidencias_bp.context_processor
def utility_processor():
    def obtener_nombre_usuario(numNomina):
        return user_model.obtener_nombre_usuario(numNomina)
    return dict(obtener_nombre_usuario=obtener_nombre_usuario)











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

@incidencias_bp.route('/cancelar_incidencia/<int:idIncidencia>', methods=['POST'])
def cancelar_incidencia(idIncidencia):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
        
    comentarios = request.form.get('comentarios', '')
    numNomina = session['numNomina']
    resultado = user_model.cancelar_incidencia(idIncidencia, numNomina, comentarios)
    
    if resultado.get('success'):
        # Obtener datos de la incidencia para notificación
        incidencia = user_model.get_incidencia_by_id(idIncidencia)
        if incidencia:
            # Notificar al solicitante
            user_model.enviar_notificacion_incidencia(
                numNomina,
                'Cancelada',
                incidencia['motivo'],
                incidencia['fecha_inicio'],
                incidencia['fecha_fin']
            )
            
            # Notificar al jefe directo si estaba pendiente
            if incidencia['estatus'] == 'Pendiente Supervisor':
                user_model.enviar_notificacion_incidencia(
                    numNomina,
                    'Solicitud cancelada por el empleado',
                    incidencia['motivo'],
                    incidencia['fecha_inicio'],
                    incidencia['fecha_fin'],
                    incidencia['jefe_directo']
                )
                
        flash("Incidencia cancelada exitosamente", "success")
    else:
        error = resultado.get('error')
        if error == 'incidencia_no_encontrada':
            flash("No se encontró la incidencia o no tienes permiso para cancelarla", "error")
        elif error == 'incidencia_ya_procesada':
            flash("Esta incidencia ya ha sido procesada y no puede cancelarse", "error")
        else:
            flash("Error al cancelar la incidencia", "error")
            
    return redirect(url_for('incidencias.mis_solicitudes'))

