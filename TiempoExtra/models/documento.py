from models.db import get_db_connection

class DocumentoFormato:
    def __init__(self, row):
        self.id = row.id
        self.usuario_id = row.usuario_id
        self.nombre_archivo = row.nombre_archivo
        self.ruta_archivo = row.ruta_archivo
        self.estado = row.estado
        self.fecha_subida = row.fecha_subida
        self.comentarios_gerencia = row.comentarios_gerencia
        self.comentarios_japones = row.comentarios_japones
        self.nomina_aprobador_1 = row.nomina_aprobador_1
        self.nomina_aprobador_2 = row.nomina_aprobador_2

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

def guardar_pdf_usuario(usuario_id, nombre_archivo, ruta_archivo, nomina_gerente):
    conn = get_db_connection()
    if not conn: 
        return False
    try:
        cursor = conn.cursor()
        
        # 1. Obtener datos del departamento del empleado
        # 🌟 CORRECCIÓN: d.id_departamento en el JOIN
        cursor.execute("""
            SELECT u.id_departamento, d.nombre_departamento 
            FROM Usuarios u
            INNER JOIN Departamentos d ON u.id_departamento = d.id_departamento
            WHERE u.num_nomina = ?
        """, (usuario_id,))
        res_usuario = cursor.fetchone()
        
        if not res_usuario:
            return False
            
        id_depto = res_usuario[0]
        nombre_depto = res_usuario[1]
        
        # 2. Buscar AUTOMÁTICAMENTE al Jefe Japonés (Con excepción para Sistemas)
        if nombre_depto.strip().lower() == 'sistemas':
            # 🌟 CORRECCIÓN: d.id_departamento en el JOIN
            cursor.execute("""
                SELECT u.num_nomina 
                FROM Usuarios u
                INNER JOIN Roles r ON u.id_rol = r.id_rol
                INNER JOIN Departamentos d ON u.id_departamento = d.id_departamento
                WHERE d.nombre_departamento = 'Administración' AND r.nombre_rol = 'Jefe Japonés'
            """)
        else:
            cursor.execute("""
                SELECT u.num_nomina 
                FROM Usuarios u
                INNER JOIN Roles r ON u.id_rol = r.id_rol
                WHERE u.id_departamento = ? AND r.nombre_rol = 'Jefe Japonés'
            """, (id_depto,))
            
        res_japones = cursor.fetchone()
        nomina_japones_automatica = res_japones[0] if res_japones else None

        # 3. Guardar el registro
        cursor.execute("""
            INSERT INTO ControlDocumentos 
            (usuario_id, nombre_archivo, ruta_archivo, estado, nomina_aprobador_1, nomina_aprobador_2, fecha_subida)
            VALUES (?, ?, ?, 'Pendiente Gerencia', ?, ?, GETDATE())
        """, (usuario_id, nombre_archivo, ruta_archivo, nomina_gerente, nomina_japones_automatica))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al guardar documento con escalación automática: {e}")
        return False
    finally:
        if conn:
            conn.close()

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
        SELECT id, usuario_id, nombre_archivo, ruta_archivo, estado, fecha_subida,
               comentarios_gerencia, comentarios_japones, nomina_aprobador_1, nomina_aprobador_2
        FROM ControlDocumentos 
        WHERE id = ?
    """, (doc_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return DocumentoFormato(row) # Convertimos el resultado al formato seguro
    return None

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

def obtener_historial_revisiones_jefe():
    conn = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor()
    # Buscamos todos los documentos que ya fueron procesados (Aprobados o Rechazados)
    cursor.execute("""
        SELECT id, usuario_id, nombre_archivo, ruta_archivo, estado, comentarios_jefe, fecha_subida, fecha_revision
        FROM ControlDocumentos 
        WHERE estado IN ('Aprobado', 'Rechazado')
        ORDER BY fecha_revision DESC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    return rows

def eliminar_documento_pendiente(doc_id, usuario_id):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    # Por seguridad, verificamos que el documento sea del usuario y siga 'Pendiente'
    cursor.execute("""
        DELETE FROM ControlDocumentos 
        WHERE id = ? AND usuario_id = ? AND estado = 'Pendiente'
    """, (doc_id, usuario_id))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def obtener_documentos_pendientes_por_rol(rol_usuario, num_nomina_sesion):
    conn = get_db_connection()
    if not conn: 
        return []
    cursor = conn.cursor()
    
    try:
        # 1. NIVEL 1: Gerentes, Supervisores y ASISTENTES DE GERENTE revisan 'Pendiente Gerencia'
        #    Sincronizado con la columna 'nomina_aprobador_1'
        if rol_usuario in ['Gerente', 'Supervisor', 'Asistente de Gerente']:
            cursor.execute("""
                SELECT id, usuario_id, nombre_archivo, ruta_archivo, estado, fecha_subida 
                FROM ControlDocumentos 
                WHERE estado = 'Pendiente Gerencia' AND nomina_aprobador_1 = ? 
                ORDER BY fecha_subida DESC
            """, (num_nomina_sesion,))
            
        # 2. NIVEL 2: El Jefe Japonés revisa 'Pendiente Jefe Japonés'
        #    Sincronizado con la columna 'nomina_aprobador_2'
        elif rol_usuario == 'Jefe Japonés':
            cursor.execute("""
                SELECT id, usuario_id, nombre_archivo, ruta_archivo, estado, fecha_subida 
                FROM ControlDocumentos 
                WHERE estado = 'Pendiente Jefe Japonés' AND nomina_aprobador_2 = ? 
                ORDER BY fecha_subida DESC
            """, (num_nomina_sesion,))
            
        # 3. ADMINISTRADOR: Súper Vista operativa (Ve todo lo pendiente sin candado de nómina)
        elif rol_usuario == 'Admin':
            cursor.execute("""
                SELECT id, usuario_id, nombre_archivo, ruta_archivo, estado, fecha_subida 
                FROM ControlDocumentos 
                WHERE estado IN ('Pendiente Gerencia', 'Pendiente Jefe Japonés') 
                ORDER BY fecha_subida DESC
            """)
        else:
            return []
            
        rows = cursor.fetchall()
        return rows
        
    except Exception as e:
        print(f"Error al obtener pendientes por rol y nómina: {e}")
        return []
    finally:
        if conn:
            conn.close()

def actualizar_voto_escalacion(doc_id, rol_aprobador, accion, comentarios):
    conn = get_db_connection()
    if not conn: return 'Error'
    cursor = conn.cursor()
    nuevo_estado = 'Rechazado'

    # 🌟 CORRECCIÓN: Agregamos 'Asistente de Gerente' a la lista de evaluación
    if rol_aprobador in ['Gerente', 'Supervisor', 'Admin', 'Asistente de Gerente']:
        nuevo_estado = 'Pendiente Jefe Japonés' if accion == 'aprobar' else 'Rechazado por Gerencia'
        cursor.execute("""
            UPDATE ControlDocumentos 
            SET estado = ?, comentarios_gerencia = ?, fecha_gerencia = GETDATE() 
            WHERE id = ?
        """, (nuevo_estado, comentarios, doc_id))
        
    elif rol_aprobador == 'Jefe Japonés':
        nuevo_estado = 'Aprobado' if accion == 'aprobar' else 'Rechazado por Jefe Japonés'
        cursor.execute("""
            UPDATE ControlDocumentos 
            SET estado = ?, comentarios_japones = ?, fecha_japones = GETDATE() 
            WHERE id = ?
        """, (nuevo_estado, comentarios, doc_id))
        
    conn.commit()
    conn.close()
    return nuevo_estado

# --- CONSULTAS AUXILIARES DE CORREOS ---
def obtener_correo_empleado_por_doc(doc_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.correo_electronico FROM ControlDocumentos d
        INNER JOIN Usuarios u ON d.usuario_id = u.num_nomina WHERE d.id = ?
    """, (doc_id,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else None

def obtener_correos_sistema_por_rol(nombre_rol):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.correo_electronico FROM Usuarios u
        INNER JOIN Roles r ON u.id_rol = r.id_rol WHERE r.nombre_rol = ?
    """, (nombre_rol,))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows if r[0]]

def obtener_documentos_usuario(usuario_id):
    """
    Obtiene todo el historial de documentos subidos por un empleado en específico.
    """
    conn = get_db_connection()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, usuario_id, nombre_archivo, ruta_archivo, estado, fecha_subida 
            FROM ControlDocumentos 
            WHERE usuario_id = ? 
            ORDER BY fecha_subida DESC
        """, (usuario_id,))
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error al obtener los documentos del usuario: {e}")
        return []
    finally:
        if conn:
            conn.close()

def cancelar_documento_pendiente(doc_id, usuario_id):
    """
    Cambia el estatus de la solicitud a 'Cancelado' en la base de datos
    sin borrar el registro ni el archivo físico del servidor.
    """
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        # Modificamos el estado a 'Cancelado' solo si sigue pendiente de gerencia
        cursor.execute("""
            UPDATE ControlDocumentos 
            SET estado = 'Cancelado' 
            WHERE id = ? AND usuario_id = ? AND estado = 'Pendiente Gerencia'
        """, (doc_id, usuario_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar estatus a Cancelado en BD: {e}")
        return False
    finally:
        if conn:
            conn.close()