import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from models.documento import obtener_pdf_usuario, guardar_pdf_usuario, obtener_todos_pdfs_usuario, obtener_documento_por_id
from werkzeug.utils import secure_filename
from models.documento import obtener_pdf_usuario, guardar_pdf_usuario

# Creamos el Blueprint para el usuario
usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/mi-documento', methods=['GET', 'POST'])
def mi_documento():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión primero.', 'danger')
        return redirect(url_for('auth.login'))
        
    usuario_id = session['usuario_id']
    
    # Manejo de la subida de un nuevo archivo (POST)
    if request.method == 'POST':
        if 'archivo_pdf' not in request.files:
            flash('No se detectó ningún archivo.', 'danger')
            return redirect(request.url)
            
        file = request.files['archivo_pdf']
        if file.filename == '':
            flash('No seleccionaste ningún archivo.', 'danger')
            return redirect(request.url)
            
        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            nuevo_nombre = f"usr_{usuario_id}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], nuevo_nombre)
            file.save(filepath)
            
            ruta_relativa = f"uploads/{nuevo_nombre}"
            
            # Guardamos en la base de datos (crea o actualiza)
            guardar_pdf_usuario(usuario_id, filename, ruta_relativa)
            
            flash('¡Documento subido exitosamente!', 'success')
            return redirect(url_for('usuario.mi_documento'))
        else:
            flash('Solo se permiten archivos .pdf', 'danger')
            return redirect(request.url)

    # --- LÓGICA PARA EL MODO LECTURA (GET) ---
    # 1. Traer la lista completa de todos sus documentos para la tabla
    mis_documentos = obtener_todos_pdfs_usuario(usuario_id)
    
    # 2. Revisar si el usuario dio clic en el botón "Detalles" de algún documento (?doc_id=X)
    doc_id = request.args.get('doc_id', type=int)
    doc_seleccionado = None
    
    if doc_id:
        doc_seleccionado = obtener_documento_por_id(doc_id)
        # Seguridad: Asegurarnos de que el documento que quiere ver sí le pertenezca a él
        if doc_seleccionado and doc_seleccionado.usuario_id != usuario_id:
            doc_seleccionado = None

    return render_template('subida_usuario.html', documentos=mis_documentos, doc_seleccionado=doc_seleccionado)