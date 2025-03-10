import datetime
import pyodbc
import smtplib
from email.mime.text import MIMEText
from flask import current_app

class UserModel:
    def __init__(self):
        self.connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=Prueba_7;"
            "UID=sa;"
            "PWD=root"
        )

    def get_connection(self):
        return pyodbc.connect(self.connection_string)

    def authenticate_user(self, login_input, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Primero verificar si existe el usuario/nómina
            if login_input.isdigit():
                query_user = "SELECT numNomina FROM usuarios WHERE numNomina = ?"
                query_credenciales = "SELECT password FROM credenciales WHERE numNomina = ?"
            else:
                query_user = "SELECT numNomina FROM credenciales WHERE username = ?"
                query_credenciales = "SELECT password FROM credenciales WHERE username = ?"

            # 1. Verificar existencia del usuario
            cursor.execute(query_user, (login_input,))
            usuario_existente = cursor.fetchone()
            if not usuario_existente:
                return {"success": False, "error": "user_not_found"}

            # 2. Verificar contraseña
            cursor.execute(query_credenciales, (login_input,))
            credencial = cursor.fetchone()
            if credencial.password != password:
                return {"success": False, "error": "wrong_password"}

            # 3. Obtener datos completos del usuario
            cursor.execute("""
                SELECT u.numNomina, u.nombre, u.apellidoPaterno, u.apellidoMaterno, 
                    c.username, r.nombreRol
                FROM usuarios u
                INNER JOIN credenciales c ON u.numNomina = c.numNomina
                INNER JOIN usuario_rol ur ON u.numNomina = ur.numNomina
                INNER JOIN roles r ON ur.idRol = r.idRol
                WHERE c.username = ? OR u.numNomina = ?
            """, (login_input, login_input))
            
            usuario = cursor.fetchone()
            return {"success": True, "data": usuario}

        except Exception as e:
            print(f"Error en autenticación: {e}")
            return {"success": False, "error": "server_error"}
        finally:
            cursor.close()
            conn.close()

    def add_user(self, numNomina, nombre, apellido_paterno, apellido_materno, username, password, idRol, idDepartamento, idPuesto, diasVacaciones):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Insertar en usuarios
            cursor.execute("""
                INSERT INTO usuarios (numNomina, nombre, apellidoPaterno, apellidoMaterno, idDepartamento, idPuesto, diasVacaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (numNomina, nombre, apellido_paterno, apellido_materno, idDepartamento, idPuesto, diasVacaciones))

            # Insertar en credenciales
            cursor.execute("""
                INSERT INTO credenciales (numNomina, username, password)
                VALUES (?, ?, ?)
            """, (numNomina, username, password))

            # Asignar rol
            cursor.execute("""
                INSERT INTO usuario_rol (numNomina, idRol)
                VALUES (?, ?)
            """, (numNomina, idRol))

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
            SELECT u.numNomina, u.nombre, u.apellidoPaterno, u.apellidoMaterno, c.username
            FROM usuarios u
            INNER JOIN credenciales c ON u.numNomina = c.numNomina
        """)
        registros = cursor.fetchall()
        cursor.close()
        conn.close()
        return registros
    
    def get_all_users_with_details(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    u.numNomina, 
                    u.nombre, 
                    u.apellidoPaterno, 
                    u.apellidoMaterno, 
                    c.username, 
                    d.nombreDepartamento, 
                    p.nombrePuesto, 
                    u.diasVacaciones  -- Asegúrate de incluir los días de vacaciones
                FROM usuarios u
                INNER JOIN credenciales c ON u.numNomina = c.numNomina
                LEFT JOIN departamentos d ON u.idDepartamento = d.idDepartamento
                LEFT JOIN puestos p ON u.idPuesto = p.idPuesto
            """)
            registros = cursor.fetchall()
            return registros
        except Exception as e:
            print(f"Error al obtener usuarios con detalles: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def update_user(self, numNomina, nombre, apellido_paterno, apellido_materno, username, idDepartamento, idPuesto, idRol, diasVacaciones):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Actualizar tabla usuarios
            cursor.execute("""
                UPDATE usuarios
                SET nombre = ?, apellidoPaterno = ?, apellidoMaterno = ?, idDepartamento = ?, idPuesto = ?, diasVacaciones = ?
                WHERE numNomina = ?
            """, (nombre, apellido_paterno, apellido_materno, idDepartamento, idPuesto, diasVacaciones, numNomina))

            # Actualizar tabla credenciales
            cursor.execute("""
                UPDATE credenciales
                SET username = ?
                WHERE numNomina = ?
            """, (username, numNomina))

            # Actualizar tabla usuario_rol
            cursor.execute("""
                UPDATE usuario_rol
                SET idRol = ?
                WHERE numNomina = ?
            """, (idRol, numNomina))

            conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_user(self, numNomina):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Eliminar de usuario_rol
            cursor.execute("DELETE FROM usuario_rol WHERE numNomina = ?", (numNomina,))
            # Eliminar de credenciales
            cursor.execute("DELETE FROM credenciales WHERE numNomina = ?", (numNomina,))
            # Eliminar de usuarios
            cursor.execute("DELETE FROM usuarios WHERE numNomina = ?", (numNomina,))
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
        
    def get_roles(self):
            conn = self.get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT idRol, nombreRol FROM roles")
                roles = cursor.fetchall()
                return roles
            except Exception as e:
                print(f"Error al obtener roles: {e}")
                return []
            finally:
                cursor.close()
                conn.close()

    def get_user_by_numNomina(self, numNomina):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    u.numNomina, 
                    u.nombre, 
                    u.apellidoPaterno, 
                    u.apellidoMaterno, 
                    c.username, 
                    u.idDepartamento, 
                    u.idPuesto, 
                    u.diasVacaciones,
                    ur.idRol  -- Asegúrate de incluir el idRol
                FROM usuarios u
                INNER JOIN credenciales c ON u.numNomina = c.numNomina
                INNER JOIN usuario_rol ur ON u.numNomina = ur.numNomina
                WHERE u.numNomina = ?
            """, (numNomina,))
            usuario = cursor.fetchone()
            if usuario:
                # Convertir el resultado en un diccionario
                usuario_dict = {
                    'numNomina': usuario.numNomina,
                    'nombre': usuario.nombre,
                    'apellidoPaterno': usuario.apellidoPaterno,
                    'apellidoMaterno': usuario.apellidoMaterno,
                    'username': usuario.username,
                    'idDepartamento': usuario.idDepartamento,
                    'idPuesto': usuario.idPuesto,
                    'diasVacaciones': usuario.diasVacaciones,
                    'idRol': usuario.idRol  # Asegúrate de incluir el idRol
                }
                return usuario_dict
            return None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_vacaciones(self, numNomina):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT diasVacaciones FROM usuarios WHERE numNomina = ?", (numNomina,))
            vacaciones = cursor.fetchone()
            return vacaciones[0] if vacaciones else 0
        except Exception as e:
            print(f"Error al obtener días de vacaciones: {e}")
            return 0
        finally:
            cursor.close()
            conn.close()

    def get_departamentos(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT idDepartamento, nombreDepartamento FROM departamentos")
        departamentos = cursor.fetchall()
        cursor.close()
        conn.close()
        return departamentos

    def get_puestos(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT idPuesto, nombrePuesto FROM puestos")
        puestos = cursor.fetchall()
        cursor.close()
        conn.close()
        return puestos
    
    def get_puestos_por_departamento(self, idDepartamento):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Obtener los puestos asociados al departamento
            cursor.execute("""
                SELECT p.idPuesto, p.nombrePuesto
                FROM puestos p
                INNER JOIN departamento_puesto dp ON p.idPuesto = dp.idPuesto
                WHERE dp.idDepartamento = ?
            """, (idDepartamento,))
            puestos = cursor.fetchall()
            return [{"idPuesto": puesto.idPuesto, "nombrePuesto": puesto.nombrePuesto} for puesto in puestos]
        except Exception as e:
            print(f"Error al obtener puestos por departamento: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_departamento_by_id(self, idDepartamento):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT nombreDepartamento FROM departamentos WHERE idDepartamento = ?", (idDepartamento,))
            departamento = cursor.fetchone()
            if departamento:
                # Convertir la fila en un diccionario
                return {'nombreDepartamento': departamento[0]}  # Acceder al primer campo usando índice 0
            return None
        except Exception as e:
            print(f"Error al obtener departamento: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_puesto_by_id(self, idPuesto):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT nombrePuesto FROM puestos WHERE idPuesto = ?", (idPuesto,))
            puesto = cursor.fetchone()
            if puesto:
                # Convertir la fila en un diccionario
                return {'nombrePuesto': puesto[0]}  # Acceder al primer campo usando índice 0
            return None
        except Exception as e:
            print(f"Error al obtener puesto: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_supervisor(self, numNomina):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT u.numNomina, u.nombre, u.apellidoPaterno, u.apellidoMaterno, c.username, u.email
                FROM usuarios u
                INNER JOIN credenciales c ON u.numNomina = c.numNomina
                WHERE u.numNomina = (
                    SELECT idSupervisor FROM usuarios WHERE numNomina = ?
                )
            """, (numNomina,))
            supervisor = cursor.fetchone()
            if supervisor:
                return {
                    'numNomina': supervisor.numNomina,
                    'nombre': supervisor.nombre,
                    'apellidoPaterno': supervisor.apellidoPaterno,
                    'apellidoMaterno': supervisor.apellidoMaterno,
                    'username': supervisor.username,
                    'email': supervisor.email
                }
            return None
        except Exception as e:
            print(f"Error al obtener supervisor: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_gerente(self, numNomina):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT u.numNomina, u.nombre, u.apellidoPaterno, u.apellidoMaterno, c.username, u.email
                FROM usuarios u
                INNER JOIN credenciales c ON u.numNomina = c.numNomina
                WHERE u.numNomina = (
                    SELECT idGerente FROM usuarios WHERE numNomina = ?
                )
            """, (numNomina,))
            gerente = cursor.fetchone()
            if gerente:
                return {
                    'numNomina': gerente.numNomina,
                    'nombre': gerente.nombre,
                    'apellidoPaterno': gerente.apellidoPaterno,
                    'apellidoMaterno': gerente.apellidoMaterno,
                    'username': gerente.username,
                    'email': gerente.email
                }
            return None
        except Exception as e:
            print(f"Error al obtener gerente: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def crear_incidencia(self, numNomina, motivo, fecha_inicio, fecha_fin, supervisor):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Obtener el correo del usuario que envía la solicitud
            cursor.execute("SELECT email FROM usuarios WHERE numNomina = ?", (numNomina,))
            usuario = cursor.fetchone()
            if not usuario:
                return False

            # Insertar la incidencia en la base de datos
            cursor.execute("""
                INSERT INTO incidencias (numNomina, motivo, fecha_inicio, fecha_fin, estado, aprobado_por_supervisor)
                VALUES (?, ?, ?, ?, 'Pendiente', ?)
            """, (numNomina, motivo, fecha_inicio, fecha_fin, supervisor))
            conn.commit()

            # Obtener el correo del supervisor
            cursor.execute("SELECT email FROM usuarios WHERE numNomina = ?", (supervisor,))
            supervisor_info = cursor.fetchone()
            if not supervisor_info:
                return False

            # Enviar correo de notificación al supervisor
            asunto = "Nueva solicitud de incidencia"
            cuerpo = f"El usuario {usuario.email} ha enviado una solicitud de incidencia. Por favor, revise y apruebe o rechace."
            self.enviar_correo(usuario.email, supervisor_info.email, asunto, cuerpo)

            return True
        except Exception as e:
            print(f"Error al crear incidencia: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def aprobar_incidencia_supervisor(self, idIncidencia, numNomina, aprobado, comentarios=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Obtener los detalles de la incidencia
            cursor.execute("""
                SELECT i.*, u.email AS email_usuario
                FROM incidencias i
                INNER JOIN usuarios u ON i.numNomina = u.numNomina
                WHERE i.idIncidencia = ?
            """, (idIncidencia,))
            incidencia = cursor.fetchone()
            if not incidencia:
                return False

            # Actualizar el estado de la incidencia
            estado = "Aprobado por Supervisor" if aprobado else "Rechazado por Supervisor"
            cursor.execute("""
                UPDATE incidencias
                SET estado = ?, aprobado_por_supervisor = ?, fecha_aprobacion_supervisor = ?, comentarios = ?
                WHERE idIncidencia = ?
            """, (estado, numNomina, datetime.now(), comentarios, idIncidencia))
            conn.commit()

            # Enviar correo de notificación al usuario
            asunto = f"Solicitud {estado}"
            cuerpo = f"Su solicitud de incidencia ha sido {estado.lower()}."
            if comentarios:
                cuerpo += f"\nComentarios: {comentarios}"
            self.enviar_correo(incidencia.email_usuario, incidencia.email_usuario, asunto, cuerpo)

            # Si se aprueba, notificar al gerente
            if aprobado:
                gerente = self.get_gerente(numNomina)
                if gerente:
                    asunto = "Nueva solicitud para aprobación"
                    cuerpo = f"El supervisor {incidencia.email_usuario} ha aprobado una solicitud de incidencia. Por favor, revise y apruebe o rechace."
                    self.enviar_correo(incidencia.email_usuario, gerente['email'], asunto, cuerpo)

            return True
        except Exception as e:
            print(f"Error al aprobar/rechazar incidencia como supervisor: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def aprobar_incidencia_gerente(self, idIncidencia, numNomina, aprobado, comentarios=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Obtener los detalles de la incidencia
            cursor.execute("""
                SELECT i.*, u.email AS email_usuario, s.email AS email_supervisor
                FROM incidencias i
                INNER JOIN usuarios u ON i.numNomina = u.numNomina
                LEFT JOIN usuarios s ON i.aprobado_por_supervisor = s.numNomina
                WHERE i.idIncidencia = ?
            """, (idIncidencia,))
            incidencia = cursor.fetchone()
            if not incidencia:
                return False

            # Actualizar el estado de la incidencia
            estado = "Aprobado por Gerente" if aprobado else "Rechazado por Gerente"
            cursor.execute("""
                UPDATE incidencias
                SET estado = ?, aprobado_por_gerente = ?, fecha_aprobacion_gerente = ?, comentarios = ?
                WHERE idIncidencia = ?
            """, (estado, numNomina, datetime.now(), comentarios, idIncidencia))
            conn.commit()

            # Enviar correo de notificación al usuario y al supervisor
            asunto = f"Solicitud {estado}"
            cuerpo = f"Su solicitud de incidencia ha sido {estado.lower()}."
            if comentarios:
                cuerpo += f"\nComentarios: {comentarios}"
            self.enviar_correo(incidencia.email_usuario, incidencia.email_usuario, asunto, cuerpo)
            if incidencia.email_supervisor:
                self.enviar_correo(incidencia.email_usuario, incidencia.email_supervisor, asunto, cuerpo)

            return True
        except Exception as e:
            print(f"Error al aprobar/rechazar incidencia como gerente: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    # Método para obtener una incidencia por su ID
    def get_incidencia_by_id(self, idIncidencia):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT i.*, u.nombre AS nombre_usuario, u.email AS email_usuario, s.email AS email_supervisor
                FROM incidencias i
                INNER JOIN usuarios u ON i.numNomina = u.numNomina
                LEFT JOIN usuarios s ON i.aprobado_por_supervisor = s.numNomina
                WHERE i.idIncidencia = ?
            """, (idIncidencia,))
            incidencia = cursor.fetchone()
            if incidencia:
                return {
                    'idIncidencia': incidencia.idIncidencia,
                    'numNomina': incidencia.numNomina,
                    'motivo': incidencia.motivo,
                    'fecha_inicio': incidencia.fecha_inicio,
                    'fecha_fin': incidencia.fecha_fin,
                    'estado': incidencia.estado,
                    'nombre_usuario': incidencia.nombre_usuario,
                    'email_usuario': incidencia.email_usuario,
                    'email_supervisor': incidencia.email_supervisor
                }
            return None
        except Exception as e:
            print(f"Error al obtener incidencia por ID: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_incidencias_enviadas(self, numNomina):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    i.idIncidencia, 
                    i.motivo, 
                    i.fecha_inicio, 
                    i.fecha_fin, 
                    i.estado, 
                    i.comentarios,
                    s.nombre AS nombre_supervisor,
                    g.nombre AS nombre_gerente
                FROM incidencias i
                LEFT JOIN usuarios s ON i.aprobado_por_supervisor = s.numNomina
                LEFT JOIN usuarios g ON i.aprobado_por_gerente = g.numNomina
                WHERE i.numNomina = ?
            """, (numNomina,))
            incidencias = cursor.fetchall()
            return incidencias
        except Exception as e:
            print(f"Error al obtener incidencias enviadas: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_incidencias_recibidas(self, numNomina):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    i.idIncidencia, 
                    i.motivo, 
                    i.fecha_inicio, 
                    i.fecha_fin, 
                    i.estado, 
                    i.comentarios,
                    u.nombre AS nombre_usuario,
                    u.email AS email_usuario
                FROM incidencias i
                INNER JOIN usuarios u ON i.numNomina = u.numNomina
                WHERE i.aprobado_por_supervisor = ? OR i.aprobado_por_gerente = ?
            """, (numNomina, numNomina))
            incidencias = cursor.fetchall()
            return incidencias
        except Exception as e:
            print(f"Error al obtener incidencias recibidas: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def enviar_correo(self, remitente, destinatario, asunto, cuerpo):
        try:
            mensaje = MIMEText(cuerpo)
            mensaje["Subject"] = asunto
            mensaje["From"] = remitente  # Correo del remitente
            mensaje["To"] = destinatario  # Correo del destinatario

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