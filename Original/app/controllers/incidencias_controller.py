import datetime
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

def crear_incidencia(self, numNomina, motivo, fecha_inicio, fecha_fin, supervisor):
    conn = self.get_connection()
    cursor = conn.cursor()
    try:
        # Obtener los días de vacaciones disponibles
        dias_vacaciones = self.get_vacaciones(numNomina)

        # Calcular el número de días solicitados
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        dias_solicitados = (fecha_fin - fecha_inicio).days + 1

        # Verificar si hay suficientes días de vacaciones
        if motivo == "vacaciones" and dias_solicitados > dias_vacaciones:
            return False  # No hay suficientes días de vacaciones

        # Insertar la incidencia en la base de datos
        cursor.execute("""
            INSERT INTO incidencias (numNomina, motivo, fecha_inicio, fecha_fin, estado, aprobado_por_supervisor)
            VALUES (?, ?, ?, ?, 'Pendiente', ?)
        """, (numNomina, motivo, fecha_inicio, fecha_fin, supervisor))
        conn.commit()

        # Restar días de vacaciones si la incidencia es por vacaciones
        if motivo == "vacaciones":
            cursor.execute("""
                UPDATE usuarios
                SET diasVacaciones = diasVacaciones - ?
                WHERE numNomina = ?
            """, (dias_solicitados, numNomina))
            conn.commit()

        # Enviar correo de notificación al supervisor
        self.enviar_correo_supervisor(numNomina, supervisor)

        return True
    except Exception as e:
        print(f"Error al crear incidencia: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


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
    fecha_solicitud = datetime.now().strftime("%Y-%m-%d")

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
        nombre_puesto=puesto_usuario['nombrePuesto'],
        no_nomina=usuario['numNomina'],
        departamento=usuario['idDepartamento'],
        nombre_departamento=departamento_usuario['nombreDepartamento'],
        dias_vacaciones=usuario['diasVacaciones'],
        puestos=puestos,
        departamentos=departamentos,
        origen=origen)


@incidencias_bp.route('/enviar_solicitud', methods=['POST'])
def enviar_solicitud():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Obtener datos del formulario
    numNomina = session['numNomina']
    motivo = request.form['motivo']
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']

    # Obtener el jefe directo (supervisor) del usuario
    supervisor = user_model.get_supervisor(numNomina)
    if not supervisor:
        flash("No se encontró un supervisor para este usuario", "error")
        return redirect(url_for('incidencias.ver_incidencias'))

    # Insertar la incidencia en la base de datos
    if user_model.crear_incidencia(numNomina, motivo, fecha_inicio, fecha_fin, supervisor['numNomina']):
        # Enviar correo de notificación al supervisor
        asunto = "Nueva solicitud de incidencia"
        cuerpo = f"El usuario {session['user']} ha enviado una solicitud de incidencia. Por favor, revise y apruebe o rechace."
        user_model.enviar_correo(supervisor['email'], asunto, cuerpo)

        flash("Solicitud enviada correctamente", "success")
    else:
        flash("Error al enviar la solicitud", "error")

    return redirect(url_for('incidencias.ver_incidencias'))

@incidencias_bp.route('/aprobar_solicitud/<int:idIncidencia>', methods=['POST'])
def aprobar_solicitud(idIncidencia):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Obtener la incidencia
    incidencia = user_model.get_incidencia_by_id(idIncidencia)
    if not incidencia:
        flash("Incidencia no encontrada", "error")
        return redirect(url_for('incidencias.incidencias_recibidas'))

    # Verificar el rol del usuario actual
    if session['rol'] == 'Supervisor':
        # Aprobar como supervisor
        if user_model.aprobar_incidencia_supervisor(idIncidencia, session['numNomina']):
            # Notificar al usuario A
            asunto = "Solicitud aprobada por supervisor"
            cuerpo = f"Su solicitud de incidencia ha sido aprobada por el supervisor."
            user_model.enviar_correo(incidencia['email_usuario'], asunto, cuerpo)

            # Notificar al gerente
            gerente = user_model.get_gerente(session['numNomina'])
            if gerente:
                asunto = "Nueva solicitud para aprobación"
                cuerpo = f"El supervisor {session['user']} ha aprobado una solicitud de incidencia. Por favor, revise y apruebe o rechace."
                user_model.enviar_correo(gerente['email'], asunto, cuerpo)

            flash("Solicitud aprobada por supervisor", "success")
        else:
            flash("Error al aprobar la solicitud", "error")

    elif session['rol'] == 'Gerente':
        # Aprobar como gerente
        if user_model.aprobar_incidencia_gerente(idIncidencia, session['numNomina']):
            # Notificar al usuario A y al supervisor
            asunto = "Solicitud aprobada por gerente"
            cuerpo = f"Su solicitud de incidencia ha sido aprobada por el gerente."
            user_model.enviar_correo(incidencia['email_usuario'], asunto, cuerpo)
            user_model.enviar_correo(incidencia['email_supervisor'], asunto, cuerpo)

            flash("Solicitud aprobada por gerente", "success")
        else:
            flash("Error al aprobar la solicitud", "error")

    return redirect(url_for('incidencias.incidencias_recibidas'))

@incidencias_bp.route('/mis_incidencias')
def mis_incidencias():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Obtener las incidencias enviadas por el usuario actual
    numNomina = session['numNomina']
    incidencias = user_model.get_incidencias_enviadas(numNomina)

    return render_template('mis_incidencias.html', incidencias=incidencias, username=session['user'])