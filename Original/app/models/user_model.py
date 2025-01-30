import pyodbc
import smtplib
from email.mime.text import MIMEText
from flask import current_app

class UserModel:
    def __init__(self):
        self.connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=Prueba_2;"
            "UID=sa;"
            "PWD=root"
        )

    def get_connection(self):
        return pyodbc.connect(self.connection_string)

    def authenticate_user(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.idUsuario, u.nombre, u.apellidoPaterno, u.apellidoMaterno, c.username
            FROM usuarios u
            INNER JOIN credenciales c ON u.idUsuario = c.idUsuario
            WHERE c.username = ? AND c.password = ?
        """, (username, password))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario

    def add_user(self, nombre, apellido_paterno, apellido_materno, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (nombre, apellidoPaterno, apellidoMaterno)
                OUTPUT INSERTED.idUsuario
                VALUES (?, ?, ?)
            """, (nombre, apellido_paterno if apellido_paterno else '', apellido_materno if apellido_materno else ''))
            id_usuario = cursor.fetchone()[0]
            cursor.execute("""
                INSERT INTO credenciales (idUsuario, username, password)
                VALUES (?, ?, ?)
            """, (id_usuario, username, password))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar usuario: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def get_all_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.idUsuario, u.nombre, u.apellidoPaterno, u.apellidoMaterno, c.username
            FROM usuarios u
            INNER JOIN credenciales c ON u.idUsuario = c.idUsuario
        """)
        registros = cursor.fetchall()
        cursor.close()
        conn.close()
        return registros

    def get_user_by_id(self, id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.idUsuario, u.nombre, u.apellidoPaterno, u.apellidoMaterno, c.username
            FROM usuarios u
            INNER JOIN credenciales c ON u.idUsuario = c.idUsuario
            WHERE u.idUsuario = ?
        """, id)
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario

    def update_user(self, id, nombre, apellido_paterno, apellido_materno, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE usuarios
                SET nombre = ?, apellidoPaterno = ?, apellidoMaterno = ?
                WHERE idUsuario = ?
            """, (nombre, apellido_paterno, apellido_materno, id))
            cursor.execute("""
                UPDATE credenciales
                SET username = ?
                WHERE idUsuario = ?
            """, (username, id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_user(self, id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM credenciales WHERE idUsuario = ?", id)
            cursor.execute("DELETE FROM usuarios WHERE idUsuario = ?", id)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al borrar usuario: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def enviar_correo(self, destinatario, asunto, cuerpo):
        try:
            # Configurar el mensaje
            mensaje = MIMEText(cuerpo)
            mensaje["Subject"] = asunto
            mensaje["From"] = current_app.config["MAIL_USERNAME"]
            mensaje["To"] = destinatario

            # Conectar al servidor SMTP
            with smtplib.SMTP(
                current_app.config["MAIL_SERVER"],
                current_app.config["MAIL_PORT"]
            ) as server:
                server.starttls()
                server.login(
                    current_app.config["MAIL_USERNAME"],
                    current_app.config["MAIL_PASSWORD"]
                )
                server.send_message(mensaje)
                
            return True
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return False
        
    def enviar_correo(self, destinatarios, asunto, cuerpo):
        try:
            mensaje = MIMEText(cuerpo)
            mensaje["Subject"] = asunto
            mensaje["From"] = current_app.config["MAIL_USERNAME"]
            mensaje["To"] = ", ".join(destinatarios)  # Unir correos con comas

            with smtplib.SMTP(
                current_app.config["MAIL_SERVER"],
                current_app.config["MAIL_PORT"]
            ) as server:
                server.starttls()
                server.login(
                    current_app.config["MAIL_USERNAME"],
                    current_app.config["MAIL_PASSWORD"]
                )
                # Enviar a todos los destinatarios
                server.sendmail(
                    current_app.config["MAIL_USERNAME"],
                    destinatarios,
                    mensaje.as_string()
                )
            return True
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return False
    

