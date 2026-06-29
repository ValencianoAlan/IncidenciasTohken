from models.db import get_db_connection

def verificar_credenciales(num_nomina, password):
    conn = get_db_connection()
    if not conn:
        return None
        
    cursor = conn.cursor()
    # Buscamos que coincida la nómina y el password
    # NOTA: Si en tu BD real las contraseñas están encriptadas, aquí usarías hash. Por ahora validamos texto plano.
    cursor.execute("""
        SELECT id, num_nomina, nombre, rol 
        FROM Usuarios 
        WHERE num_nomina = ? AND password = ?
    """, (num_nomina, password))
    
    usuario = cursor.fetchone()
    conn.close()
    return usuario # Devuelve el registro si coincide, o None si no coincide