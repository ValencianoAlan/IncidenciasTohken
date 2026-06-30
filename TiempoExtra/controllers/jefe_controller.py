from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from models.usuario import agregar_nuevo_usuario, obtener_todos_los_usuarios, obtener_todos_los_roles, obtener_todos_los_departamentos

from models.documento import obtener_documentos_pendientes, obtener_documento_por_id, actualizar_estado_documento, obtener_historial_revisiones_jefe

from models.usuario import obtener_usuario_por_nomina, obtener_todos_jefes_japoneses # 🌟 IMPORTAR LA NUEVA FUNCIÓN

from utils.correo import enviar_correo_escalacion
from models.documento import (
    obtener_documentos_pendientes_por_rol, obtener_documento_por_id, 
    actualizar_voto_escalacion, obtener_correo_empleado_por_doc, obtener_correos_sistema_por_rol
)

from models.documento import obtener_documentos_pendientes_por_rol, obtener_documento_por_id, obtener_historial_dictamenes_por_jefe # 🌟 IMPORTAR LA NUEVA FUNCIÓN

jefe_bp = Blueprint('jefe', __name__)

@jefe_bp.route('/panel-jefe', methods=['GET'])
def panel():
    if 'usuario_id' not in session or session.get('rol') not in ['Admin', 'Gerente', 'Supervisor', 'Asistente de Gerente', 'Jefe Japonés']:
        flash('🚫 Acceso denegado.', 'danger')
        return redirect(url_for('auth.menu'))
        
    rol_usuario = session['rol']
    nomina_usuario = session['num_nomina']
    
    # Aquí el modelo ya sabe qué hacer si detecta que eres 'Admin'
    documentos_pendientes = obtener_documentos_pendientes_por_rol(rol_usuario, nomina_usuario)
    documentos_historial = obtener_historial_dictamenes_por_jefe(rol_usuario, nomina_usuario)
    
    doc_id = request.args.get('doc_id', type=int)
    doc_seleccionado = None
    if doc_id:
        doc_seleccionado = obtener_documento_por_id(doc_id)
        
    jefes_japoneses = obtener_todos_jefes_japoneses()
        
    return render_template('panel_jefe.html', 
                           documentos=documentos_pendientes, 
                           historial=documentos_historial, 
                           doc_seleccionado=doc_seleccionado, 
                           japoneses=jefes_japoneses)

@jefe_bp.route('/procesar-documento/<int:doc_id>', methods=['POST'])
def procesar_documento(doc_id):
    rol_actual = session.get('rol')
    if 'usuario_id' not in session or rol_actual not in ['Admin', 'Gerente', 'Supervisor', 'Asistente de Gerente', 'Jefe Japonés']:
        flash('🚫 Acceso denegado.', 'danger')
        return redirect(url_for('auth.menu'))
        
    accion = request.form.get('accion')
    comentarios = request.form.get('comentarios', 'Sin comentarios adicionales.')
    nomina_japones_elegido = request.form.get('aprobador_2') # 🌟 ATRAPAMOS AL JAPONÉS ELEGIDO
    
    doc = obtener_documento_por_id(doc_id)
    if not doc:
        flash('Documento no encontrado.', 'danger')
        return redirect(url_for('jefe.panel'))
    
    # 1. Guardar en Base de Datos (enviándole el japonés)
    nuevo_estado = actualizar_voto_escalacion(doc_id, rol_actual, accion, comentarios, nomina_japones_elegido)
    
    correo_empleado = obtener_correo_empleado_por_doc(doc_id)
    correos_gerentes = obtener_correos_sistema_por_rol('Gerente') + obtener_correos_sistema_por_rol('Supervisor')
    correos_rh = obtener_correos_sistema_por_rol('RH')

    # =================================================================
    # ✉️ MOTOR DE DECISIONES DE NOTIFICACIÓN POR CORREO
    # =================================================================
    if rol_actual in ['Gerente', 'Supervisor', 'Admin', 'Asistente de Gerente'] and doc.estado == 'Pendiente Gerencia':
        if accion == 'rechazar':
            asunto = f"❌ Solicitud de Tiempo Extra Rechazada por Gerencia (Doc #{doc_id})"
            cuerpo = f"<h3>Tu formato de tiempo extra '{doc.nombre_archivo}' ha sido rechazado.</h3><p><strong>Motivo:</strong> {comentarios}</p>"
            enviar_correo_escalacion(correo_empleado, asunto, cuerpo)
            
        elif accion == 'aprobar' and nomina_japones_elegido:
            # Notificar al empleado
            asunto_emp = f"✅ Tu Solicitud de Tiempo Extra Avanzó a Jefatura Japonesa (Doc #{doc_id})"
            cuerpo_emp = f"<h3>Tu formato '{doc.nombre_archivo}' fue aprobado en primer nivel.</h3>"
            enviar_correo_escalacion(correo_empleado, asunto_emp, cuerpo_emp)
            
            # 🌟 Notificar EXCLUSIVAMENTE al Jefe Japonés elegido
            japones_info = obtener_usuario_por_nomina(nomina_japones_elegido)
            if japones_info:
                correo_jap = japones_info['correo_electronico']
                asunto_jap = f"🔔 [URGENTE] Nueva Solicitud de Tiempo Extra por Autorizar (Doc #{doc_id})"
                cuerpo_jap = f"<h3>Se ha aprobado un formato de tiempo extra en tu departamento y requiere tu autorización final.</h3><p><strong>Archivo:</strong> {doc.nombre_archivo}</p>"
                enviar_correo_escalacion(correo_jap, asunto_jap, cuerpo_jap)

    elif rol_actual == 'Jefe Japonés':
        if accion == 'rechazar':
            asunto = f"❌ Solicitud Rechazada por Dirección Japonesa (Doc #{doc_id})"
            cuerpo = f"<h3>El formato de tiempo extra '{doc.nombre_archivo}' ha sido rechazado en la instancia final.</h3><p><strong>Motivo:</strong> {comentarios}</p>"
            enviar_correo_escalacion([correo_empleado] + correos_gerentes, asunto, cuerpo)
            
        elif accion == 'aprobar':
            asunto = f"🎉 ¡Solicitud de Tiempo Extra Autorizada! (Doc #{doc_id})"
            cuerpo = f"<h3>El formato '{doc.nombre_archivo}' completó todos los niveles de escalación.</h3>"
            enviar_correo_escalacion([correo_empleado] + correos_gerentes + correos_rh, asunto, cuerpo)

    flash('Dictamen procesado exitosamente.', 'success')
    return redirect(url_for('jefe.panel'))

@jefe_bp.route('/historial-jefe', methods=['GET'])
def historial():
    if 'usuario_id' not in session or session.get('rol') not in ['Admin', 'Gerente', 'Asistente de Gerente']:
        flash('🚫 Acceso denegado.', 'danger')
        return redirect(url_for('auth.menu'))

    historial_docs = obtener_historial_revisiones_jefe()
    doc_id = request.args.get('doc_id', type=int)
    doc_seleccionado = None
    if doc_id:
        doc_seleccionado = obtener_documento_por_id(doc_id)
        
    return render_template('historial_jefe.html', documentos=historial_docs, doc_seleccionado=doc_seleccionado)


# ==========================================
# MÓDULOS DE ADMINISTRACIÓN DE USUARIOS (SOLO ADMIN)
# ==========================================

@jefe_bp.route('/usuarios/agregar', methods=['GET', 'POST'])
def agregar_usuario_vista():
    if 'usuario_id' not in session or session.get('rol') != 'Admin':
        flash('🚫 Acceso denegado. Se requieren permisos de Administrador.', 'danger')
        return redirect(url_for('auth.menu'))
        
    if request.method == 'POST':
        num_nomina = request.form.get('num_nomina')
        nombre = request.form.get('nombre')
        apellido_paterno = request.form.get('apellidoPaterno')
        apellido_materno = request.form.get('apellidoMaterno')
        username = request.form.get('username')
        password = request.form.get('password')
        id_departamento = request.form.get('id_departamento')
        puesto = request.form.get('puesto')
        dias_vacaciones = request.form.get('diasVacaciones', 0)
        correo = request.form.get('correo_electronico')
        id_rol = request.form.get('id_rol')
        
        exito = agregar_nuevo_usuario(num_nomina, nombre, apellido_paterno, apellido_materno, username, password, id_departamento, puesto, dias_vacaciones, correo, id_rol)
        
        if exito:
            flash('👤 ¡Usuario registrado exitosamente!', 'success')
            return redirect(url_for('jefe.ver_usuarios_vista'))
        else:
            flash('Error al registrar. Verifica duplicados de nómina o usuario.', 'danger')
            
    roles_cat = obtener_todos_los_roles()
    deptos_cat = obtener_todos_los_departamentos()
    return render_template('agregar_usuario.html', roles=roles_cat, departamentos=deptos_cat)

@jefe_bp.route('/usuarios/ver', methods=['GET'])
def ver_usuarios_vista():
    if 'usuario_id' not in session or session.get('rol') != 'Admin':
        flash('🚫 Acceso denegado. Se requieren permisos de Administrador.', 'danger')
        return redirect(url_for('auth.menu'))
        
    usuarios_lista = obtener_todos_los_usuarios()
    # 📑 ASEGURAMOS QUE PONGA EL ARCHIVO CORRECTO DE LA TABLA
    return render_template('ver_usuarios.html', usuarios=usuarios_lista)