from models.db import get_db_connection

print("Intentando conectar a la base de datos...")

# Llamamos a la función
conexion = get_db_connection()

if conexion:
    print("✅ ¡ÉXITO! La conexión a SQL Server está funcionando perfectamente.")
    # Cerramos la conexión para no dejar procesos abiertos
    conexion.close()
else:
    print("❌ ERROR: No se pudo conectar. Revisa los datos en config.py (Servidor, BD, Usuario o Contraseña).")