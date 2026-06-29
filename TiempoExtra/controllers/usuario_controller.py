import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session, send_from_directory
from werkzeug.utils import secure_filename

# Importaciones de Base de Datos y Correos
from models.documento import guardar_pdf_usuario, obtener_documento_por_id, eliminar_documento_pendiente
from models.usuario import (
    obtener_aprobadores_nivel_1, 
    obtener_aprobadores_nivel_2, 
    obtener_usuario_por_nomina, 
    obtener_correos_por_rol_y_depto
)
from utils.correo import enviar_correo_escalacion

usuario_bp = Blueprint('usuario', __name__)

# ==========================================
# RUTA PRINCIPAL: MIS DOCUMENTOS (SUBIDA Y VISUALIZACIÓN)
# ==========================================
@usuario_bp.route('/mis-documentos', methods=['GET', 'POST'])
def mi_documento():
    # 🔒 Seguridad: Debe estar logueado
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
        
    num_nomina = session['num_nomina']
    
    # Obtenemos los datos del usuario logueado para saber de qué departamento es
    usuario_actual = obtener_usuario_por_nomina(num_nomina)
    if not usuario_actual:
        flash('Error al cargar la información del usuario.', 'danger')
        return redirect(url_for('auth.menu'))
        
    id_depto = usuario_actual['id_departamento']
    
    # ----------------------------------------------------
    # BLOQUE POST: CUANDO EL USUARIO ENVÍA EL FORMULARIO
    # ----------------------------------------------------
    if request.method == 'POST':
        archivo = request.files.get('archivo_pdf')
        nomina_aprobador_1 = request.form.get('aprobador_1')
        # 🌟 ELIMINADO: Ya no atrapamos aprobador_2 desde el request.form
        
        if archivo and archivo.filename.endswith('.pdf') and nomina_aprobador_1:
            nombre_original = secure_filename(archivo.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            nombre_unico = f"usr_{num_nomina}_{timestamp}_{nombre_original}"
            
            directorio_destino = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(directorio_destino, exist_ok=True)
            ruta_fisica = os.path.join(directorio_destino, nombre_unico)
            archivo.save(ruta_fisica)
            
            ruta_db = f"uploads/{nombre_unico}"
            
            # 🚀 LLAMADA ACTUALIZADA: Solo le pasamos nomina_aprobador_1
            guardar_pdf_usuario(num_nomina, nombre_original, ruta_db, nomina_aprobador_1)
            
            # =======================================================
            # ✉️ LÓGICA DE CORREOS DE NOTIFICACIÓN INICIAL
            # =======================================================
            aprobador_1_info = obtener_usuario_por_nomina(nomina_aprobador_1)
            if aprobador_1_info:
                # Avisarle al Asistente o Gerente elegido
                correo_aprobador_1 = aprobador_1_info['correo_electronico']
                asunto_tarea = f"🔔 Nueva Solicitud de Tiempo Extra de {session.get('nombre_usuario')}"
                cuerpo_tarea = f"<h3>Tienes un nuevo documento PDF por revisar.</h3><p>El empleado <strong>{session.get('nombre_usuario')}</strong> ha subido un formato de tiempo extra que requiere tu autorización.</p>"
                enviar_correo_escalacion(correo_aprobador_1, asunto_tarea, cuerpo_tarea)
                
                # Alerta FYI al Gerente si revisa el Asistente
                if aprobador_1_info['nombre_rol'] == 'Asistente de Gerente':
                    correos_gerentes = obtener_correos_por_rol_y_depto('Gerente', id_depto)
                    if correos_gerentes:
                        asunto_fyi = "📋 [INFO] Solicitud recibida por tu Asistente"
                        cuerpo_fyi = f"<p>Para tu información: El empleado {session.get('nombre_usuario')} ha enviado una solicitud de tiempo extra a tu Asistente de Gerente ({aprobador_1_info['nombre']}).</p>"
                        enviar_correo_escalacion(correos_gerentes, asunto_fyi, cuerpo_fyi)

            flash('✅ Documento subido y notificaciones enviadas correctamente.', 'success')
            return redirect(url_for('usuario.mi_documento'))

    # ----------------------------------------------------
    # BLOQUE GET: CARGAR LA PANTALLA NORMAL
    # ----------------------------------------------------
    # Traemos las listas de jefes que corresponden SOLO al departamento del empleado
    aprobadores_1 = obtener_aprobadores_nivel_1(id_depto)
    aprobadores_2 = obtener_aprobadores_nivel_2(id_depto)
    
    # NOTA: Importa/crea una función que traiga solo los documentos de este usuario
    from models.documento import obtener_documentos_usuario
    documentos = obtener_documentos_usuario(num_nomina)
    
    doc_id = request.args.get('doc_id', type=int)
    doc_seleccionado = None
    if doc_id:
        doc_seleccionado = obtener_documento_por_id(doc_id)
        
    return render_template('subida_usuario.html', documentos=documentos, doc_seleccionado=doc_seleccionado, aprobadores_1=aprobadores_1, aprobadores_2=aprobadores_2)

# ==========================================
# RUTA: CANCELAR SOLICITUD (CAMBIA ESTATUS A CANCELADO)
# ==========================================
@usuario_bp.route('/eliminar-documento/<int:doc_id>', methods=['POST'])
def eliminar_documento(doc_id):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
        
    num_nomina = session['num_nomina']
    doc = obtener_documento_por_id(doc_id)
    
    # Verificamos que la solicitud exista, le pertenezca al usuario y esté en el primer nivel
    if doc and str(doc.usuario_id).strip() == str(num_nomina).strip() and str(doc.estado).strip() == 'Pendiente Gerencia':
        
        # 🌟 NUEVA LÓGICA: No tocamos el archivo PDF del servidor.
        # Solo actualizamos el estado a 'Cancelado' en la base de datos.
        from models.documento import cancelar_documento_pendiente
        exito = cancelar_documento_pendiente(doc_id, num_nomina)
        
        if exito:
            flash('🚫 La solicitud ha sido cancelada y su estatus se actualizó a Cancelado.', 'success')
        else:
            flash('Hubo un problema al actualizar el estatus en el sistema.', 'danger')
    else:
        flash('No se puede cancelar un documento que ya avanzó de nivel o fue revisado.', 'danger')
        
    return redirect(url_for('usuario.mi_documento'))

# ==========================================
# RUTA: DESCARGAR EL PDF ORIGINAL
# ==========================================
@usuario_bp.route('/descargar-pdf/<int:doc_id>')
def descargar_pdf(doc_id):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
        
    doc = obtener_documento_por_id(doc_id)
    if not doc:
        flash('El archivo no existe.', 'danger')
        return redirect(url_for('auth.menu'))
        
    # 🌟 CORRECCIÓN AQUÍ TAMBIÉN:
    nombre_archivo_fisico = os.path.basename(doc.ruta_archivo)
    directorio_uploads = os.path.join(current_app.root_path, 'static', 'uploads')
    
    return send_from_directory(
        directory=directorio_uploads, 
        path=nombre_archivo_fisico, 
        as_attachment=True, 
        download_name=doc.nombre_archivo
    )

