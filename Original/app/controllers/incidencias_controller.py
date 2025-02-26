from flask import Blueprint, render_template, request, flash, redirect, url_for, session

incidencias_bp = Blueprint('incidencias', __name__)

@incidencias_bp.route('/ver_incidencias')
def ver_incidencias():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('incidencia.html')

@incidencias_bp.route('/crear_incidencia', methods=['POST'])
def crear_incidencia():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    # Obtener datos del formulario
    nombre = request.form.get('nombre')
    apellido_paterno = request.form.get('apellido_paterno')
    apellido_materno = request.form.get('apellido_materno')
    fecha_solicitud = request.form.get('fecha_solicitud')
    puesto = request.form.get('puesto')
    no_nomina = request.form.get('no_nomina')
    departamento = request.form.get('departamento')
    motivo = request.form.get('motivo')
    num_dias = request.form.get('num_dias')
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')
    comentarios = request.form.get('comentarios')

    # Validar datos (puedes agregar más validaciones aquí)
    if not all([nombre, apellido_paterno, apellido_materno, fecha_solicitud, puesto, no_nomina, departamento, motivo, num_dias, fecha_inicio, fecha_fin, comentarios]):
        flash("Por favor, completa todos los campos obligatorios", "error")
        return redirect(url_for('incidencias.ver_incidencias'))

    # Guardar la incidencia en la base de datos (implementa esta función en el modelo)
    if user_model.crear_incidencia(nombre, apellido_paterno, apellido_materno, fecha_solicitud, puesto, no_nomina, departamento, motivo, num_dias, fecha_inicio, fecha_fin, comentarios):
        flash("Incidencia creada exitosamente", "success")
    else:
        flash("Error al crear la incidencia", "error")

    return redirect(url_for('incidencias.ver_incidencias'))