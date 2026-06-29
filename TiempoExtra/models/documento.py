from models.db import get_db_connection

def obtener_pdf_usuario(usuario_id):
    conn = get_db_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre_archivo, ruta_archivo, estado, comentarios_jefe 
        FROM ControlDocumentos 
        WHERE usuario_id = ?
    """, (usuario_id,))
    
    # fetchone() trae el primer registro encontrado
    row = cursor.fetchone()
    conn.close()
    return row

def guardar_pdf_usuario(usuario_id, nombre_archivo, ruta_archivo):
    conn = get_db_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()
    
    # Revisamos si el usuario ya tenía un documento antes
    cursor.execute("SELECT id FROM ControlDocumentos WHERE usuario_id = ?", (usuario_id,))
    existe = cursor.fetchone()
    
    if existe:
        # Si ya existe, actualizamos el registro y lo regresamos a 'Pendiente'
        cursor.execute("""
            UPDATE ControlDocumentos 
            SET nombre_archivo = ?, ruta_archivo = ?, estado = 'Pendiente', comentarios_jefe = NULL, fecha_subida = GETDATE()
            WHERE usuario_id = ?
        """, (nombre_archivo, ruta_archivo, usuario_id))
    else:
        # Si es la primera vez, hacemos un INSERT nuevo
        cursor.execute("""
            INSERT INTO ControlDocumentos (usuario_id, nombre_archivo, ruta_archivo, estado) 
            VALUES (?, ?, ?, 'Pendiente')
        """, (usuario_id, nombre_archivo, ruta_archivo))
        
    conn.commit()
    conn.close()
    return True

def obtener_documentos_pendientes():
    conn = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor()
    # Buscamos todos los que tengan estado Pendiente
    cursor.execute("""
        SELECT id, usuario_id, nombre_archivo, ruta_archivo, estado, fecha_subida 
        FROM ControlDocumentos 
        WHERE estado = 'Pendiente'
        ORDER BY fecha_subida ASC
    """)
    
    # fetchall() trae todos los registros en forma de lista
    rows = cursor.fetchall()
    conn.close()
    return rows

def obtener_documento_por_id(doc_id):
    conn = get_db_connection()
    if not conn:
        return None
        
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, usuario_id, nombre_archivo, ruta_archivo, estado, comentarios_jefe 
        FROM ControlDocumentos 
        WHERE id = ?
    """, (doc_id,))
    
    row = cursor.fetchone()
    conn.close()
    return row

def actualizar_estado_documento(doc_id, estado, comentarios):
    conn = get_db_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE ControlDocumentos 
        SET estado = ?, comentarios_jefe = ?, fecha_revision = GETDATE()
        WHERE id = ?
    """, (estado, comentarios, doc_id))
    
    conn.commit()
    conn.close()
    return True

def obtener_todos_pdfs_usuario(usuario_id):
    conn = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre_archivo, ruta_archivo, estado, comentarios_jefe, fecha_subida 
        FROM ControlDocumentos 
        WHERE usuario_id = ?
        ORDER BY fecha_subida DESC
    """, (usuario_id,))
    
    rows = cursor.fetchall()
    conn.close()
    return rows