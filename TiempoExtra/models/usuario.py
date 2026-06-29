from models.db import get_db_connection

def verificar_credenciales(num_nomina, password):
    conn = get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    # Hacemos JOIN con Roles para guardar el string real ('Admin', 'Gerente', etc.) en la sesión
    cursor.execute("""
        SELECT u.id, u.num_nomina, 
               u.nombre + ' ' + ISNULL(u.apellido_paterno, '') AS nombre, 
               r.nombre_rol
        FROM Usuarios u
        INNER JOIN Roles r ON u.id_rol = r.id_rol
        WHERE u.num_nomina = ? AND u.password = ?
    """, (num_nomina, password))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

# Agrégalas al final de models/usuario.py

def obtener_usuario_por_nomina(num_nomina):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.num_nomina, u.nombre, u.id_departamento, u.correo_electronico, r.nombre_rol 
        FROM Usuarios u
        INNER JOIN Roles r ON u.id_rol = r.id_rol
        WHERE u.num_nomina = ?
    """, (num_nomina,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'id': row.id, 'num_nomina': row.num_nomina, 'nombre': row.nombre, 
            'id_departamento': row.id_departamento, 'correo_electronico': row.correo_electronico, 
            'nombre_rol': row.nombre_rol
        }
    return None

def obtener_correos_por_rol_y_depto(nombre_rol, id_departamento):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.correo_electronico FROM Usuarios u
        INNER JOIN Roles r ON u.id_rol = r.id_rol
        WHERE r.nombre_rol = ? AND u.id_departamento = ?
    """, (nombre_rol, id_departamento))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows if r[0]]

def obtener_todos_los_roles():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    cursor.execute("SELECT id_rol, nombre_rol FROM Roles")
    rows = cursor.fetchall()
    conn.close()
    return rows

def obtener_todos_los_departamentos():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    cursor.execute("SELECT id_departamento, nombre_departamento FROM Departamentos")
    rows = cursor.fetchall()
    conn.close()
    return rows

def agregar_nuevo_usuario(num_nomina, nombre, apellido_paterno, apellido_materno, username, password, id_departamento, puesto, dias_vacaciones, correo_electronico, id_rol):
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Usuarios (num_nomina, nombre, apellido_paterno, apellido_materno, username, password, id_departamento, puesto, dias_vacaciones, correo_electronico, id_rol)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (num_nomina, nombre, apellido_paterno, apellido_materno, username, password, id_departamento, puesto, dias_vacaciones, correo_electronico, id_rol))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al agregar usuario: {e}")
        return False
    finally:
        conn.close()

def obtener_todos_los_usuarios():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    # JOIN para mostrar los nombres legibles en la tabla sin el jefe directo
    cursor.execute("""
        SELECT u.id, u.num_nomina, u.nombre, u.apellido_paterno, u.apellido_materno, 
               u.username, d.nombre_departamento, u.puesto, u.dias_vacaciones, u.correo_electronico, r.nombre_rol
        FROM Usuarios u
        INNER JOIN Departamentos d ON u.id_departamento = d.id_departamento
        INNER JOIN Roles r ON u.id_rol = r.id_rol
        ORDER BY u.nombre ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def obtener_aprobadores_nivel_1(id_departamento):
    """Trae a los Asistentes de Gerente y Gerentes. Aplica excepción para Sistemas."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 🌟 CORRECCIÓN: Usamos id_departamento en lugar de id
    cursor.execute("SELECT nombre_departamento FROM Departamentos WHERE id_departamento = ?", (id_departamento,))
    depto = cursor.fetchone()
    nombre_depto = depto[0] if depto else ""

    if nombre_depto.strip().lower() == 'sistemas':
        # 🌟 CORRECCIÓN: d.id_departamento en el JOIN
        cursor.execute("""
            SELECT u.num_nomina, u.nombre, ISNULL(u.apellido_paterno, '') AS apellido, r.nombre_rol 
            FROM Usuarios u
            INNER JOIN Roles r ON u.id_rol = r.id_rol
            INNER JOIN Departamentos d ON u.id_departamento = d.id_departamento
            WHERE d.nombre_departamento = 'Administración' AND r.nombre_rol IN ('Gerente', 'Asistente de Gerente')
        """)
    else:
        cursor.execute("""
            SELECT u.num_nomina, u.nombre, ISNULL(u.apellido_paterno, '') AS apellido, r.nombre_rol 
            FROM Usuarios u
            INNER JOIN Roles r ON u.id_rol = r.id_rol
            WHERE u.id_departamento = ? AND r.nombre_rol IN ('Gerente', 'Asistente de Gerente')
        """, (id_departamento,))
        
    rows = cursor.fetchall()
    conn.close()
    return rows

def obtener_aprobadores_nivel_2(id_departamento):
    """Trae a los Jefes Japoneses. Aplica excepción para Sistemas."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 🌟 CORRECCIÓN: Usamos id_departamento en lugar de id
    cursor.execute("SELECT nombre_departamento FROM Departamentos WHERE id_departamento = ?", (id_departamento,))
    depto = cursor.fetchone()
    nombre_depto = depto[0] if depto else ""

    if nombre_depto.strip().lower() == 'sistemas':
        # 🌟 CORRECCIÓN: d.id_departamento en el JOIN
        cursor.execute("""
            SELECT u.num_nomina, u.nombre, ISNULL(u.apellido_paterno, '') AS apellido, r.nombre_rol 
            FROM Usuarios u
            INNER JOIN Roles r ON u.id_rol = r.id_rol
            INNER JOIN Departamentos d ON u.id_departamento = d.id_departamento
            WHERE d.nombre_departamento = 'Administración' AND r.nombre_rol = 'Jefe Japonés'
        """)
    else:
        cursor.execute("""
            SELECT u.num_nomina, u.nombre, ISNULL(u.apellido_paterno, '') AS apellido, r.nombre_rol 
            FROM Usuarios u
            INNER JOIN Roles r ON u.id_rol = r.id_rol
            WHERE u.id_departamento = ? AND r.nombre_rol = 'Jefe Japonés'
        """, (id_departamento,))
        
    rows = cursor.fetchall()
    conn.close()
    return rows