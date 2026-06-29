from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.documento import obtener_documentos_pendientes, obtener_documento_por_id, actualizar_estado_documento

# Creamos el Blueprint para el jefe
jefe_bp = Blueprint('jefe', __name__)

@jefe_bp.route('/panel-jefe', methods=['GET'])
def panel():
    # 1. Traer la lista de todos los PDFs pendientes
    documentos = obtener_documentos_pendientes()
    
    # 2. Revisar si el jefe hizo clic en algún documento (viene en la URL como ?doc_id=5)
    doc_id = request.args.get('doc_id', type=int)
    doc_seleccionado = None
    
    # Si hay un ID en la URL, buscamos ese PDF específico para mostrarlo
    if doc_id:
        doc_seleccionado = obtener_documento_por_id(doc_id)
        
    return render_template('panel_jefe.html', documentos=documentos, doc_seleccionado=doc_seleccionado)


@jefe_bp.route('/procesar-documento/<int:doc_id>', methods=['POST'])
def procesar_documento(doc_id):
    # Saber qué botón presionó el jefe (viene del input hidden 'accion' en el HTML)
    accion = request.form.get('accion')
    
    if accion == 'aprobar':
        # Cambiamos estado a Aprobado, sin comentarios
        actualizar_estado_documento(doc_id, 'Aprobado', None)
        flash('✅ Documento aprobado correctamente.', 'success')
        
    elif accion == 'rechazar':
        # Capturamos el texto del textarea del modal
        comentarios = request.form.get('comentarios')
        actualizar_estado_documento(doc_id, 'Rechazado', comentarios)
        flash('❌ Documento rechazado. Se ha notificado el motivo al empleado.', 'danger')
        
    # Recargamos la pantalla del jefe (limpiando la selección)
    return redirect(url_for('jefe.panel'))