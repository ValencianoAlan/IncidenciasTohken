import os

class Config:
    SECRET_KEY = 'tu_clave_secreta_super_segura' # Necesaria para las sesiones de Flask
    
    # Ruta de la carpeta donde se guardarán los PDFs
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Límite de 16 MB por PDF
    
    # Credenciales de SQL Server
    DB_SERVER = 'PC-052\SQLEXPRESS' # Ej: 'localhost\SQLEXPRESS'
    DB_NAME = 'TE1'
    DB_USER = 'sa'
    DB_PASSWORD = 'root'
    
    # Cadena de conexión para pyodbc
    DB_CONNECTION_STRING = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}"