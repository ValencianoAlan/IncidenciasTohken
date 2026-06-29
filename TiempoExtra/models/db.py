import pyodbc
from config import Config

def get_db_connection():
    """
    Establece y retorna la conexión a SQL Server.
    """
    try:
        conn = pyodbc.connect(Config.DB_CONNECTION_STRING)
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None