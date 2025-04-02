import pyodbc
import smtplib
from email.mime.text import MIMEText
from flask import current_app

class UserModel:
    def __init__(self):
        self.connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=Prueba_10;"
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

    def add_user(self, numNomina, nombre, apellido_paterno, apellido_materno, 
                username, password, idRol, idDepartamento, idPuesto, 
                diasVacaciones, correo_electronico, jefe_directo):
        """Agrega un nuevo usuario con todos los campos requeridos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Validar campos requeridos
            if not all([numNomina, nombre, username, password, idRol, 
                    idDepartamento, idPuesto, correo_electronico]):
                raise ValueError("Todos los campos obligatorios deben ser proporcionados")

            # Insertar usuario
            cursor.execute("""
                INSERT INTO usuarios (
                    numNomina, nombre, apellidoPaterno, apellidoMaterno,
                    idDepartamento, idPuesto, diasVacaciones, 
                    correo_electronico, jefe_directo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (numNomina, nombre, apellido_paterno, apellido_materno,
                idDepartamento, idPuesto, diasVacaciones,
                correo_electronico, jefe_directo))

            # Insertar credenciales
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
            conn.rollback()
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

    def update_user(self, numNomina, nombre, apellido_paterno, apellido_materno, username, password, idDepartamento, idPuesto, idRol, diasVacaciones, correo_electronico, jefe_directo):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Actualizar tabla usuarios
            cursor.execute("""
                UPDATE usuarios
                SET nombre = ?, apellidoPaterno = ?, apellidoMaterno = ?, idDepartamento = ?, idPuesto = ?, diasVacaciones = ?, correo_electronico = ?, jefe_directo = ?
                WHERE numNomina = ?
            """, (nombre, apellido_paterno, apellido_materno, idDepartamento, idPuesto, diasVacaciones, correo_electronico, jefe_directo, numNomina))

            # Actualizar tabla credenciales
            cursor.execute("""
                UPDATE credenciales
                SET username = ?
                WHERE numNomina = ?
            """, (username, numNomina))

            # Actualizar tabla credenciales
            cursor.execute("""
                UPDATE credenciales
                SET password = ?
                WHERE numNomina = ?
            """, (password, numNomina))

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
                    c.password, 
                    u.idDepartamento, 
                    u.idPuesto, 
                    u.diasVacaciones,
                    ur.idRol,
                    u.correo_electronico,
                    u.jefe_directo
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
                    'password': usuario.password,
                    'idDepartamento': usuario.idDepartamento,
                    'idPuesto': usuario.idPuesto,
                    'diasVacaciones': usuario.diasVacaciones,
                    'idRol': usuario.idRol,
                    'correo_electronico': usuario.correo_electronico,
                    'jefe_directo': usuario.jefe_directo,
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
        cursor.execute("SELECT diasVacaciones FROM vacaciones WHERE numNomina = ?", (numNomina,))
        vacaciones = cursor.fetchone()
        cursor.close()
        conn.close()
        return vacaciones[0] if vacaciones else 0

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
                    u.diasVacaciones,
                    r.nombreRol,               -- Nuevo campo: rol
                    u.correo_electronico,       -- Nuevo campo: correo electrónico
                    j.nombre AS nombre_jefe,    -- Nuevo campo: nombre del jefe directo
                    j.apellidoPaterno AS apellido_jefe
                FROM usuarios u
                INNER JOIN credenciales c ON u.numNomina = c.numNomina
                LEFT JOIN departamentos d ON u.idDepartamento = d.idDepartamento
                LEFT JOIN puestos p ON u.idPuesto = p.idPuesto
                LEFT JOIN usuario_rol ur ON u.numNomina = ur.numNomina
                LEFT JOIN roles r ON ur.idRol = r.idRol
                LEFT JOIN usuarios j ON u.jefe_directo = j.numNomina  -- Join para obtener el jefe directo
            """)

            registros = cursor.fetchall()
            return registros
        except Exception as e:
            print(f"Error al obtener usuarios con detalles: {e}")
            return []
        finally:
            cursor.close()
            conn.close()





    def get_solicitudes_enviadas(self, numNomina, orden='asc'):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                SELECT 
                    idIncidencia,
                    numNomina_solicitante,
                    fecha_solicitud,
                    motivo,
                    estatus
                FROM incidencias
                WHERE numNomina_solicitante = ?
                ORDER BY idIncidencia {}  -- Ordenar por ID
            """.format('ASC' if orden == 'asc' else 'DESC')

            cursor.execute(query, (numNomina,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener solicitudes enviadas: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_solicitudes_recibidas(self, numNomina_jefe, rol_usuario, orden='asc'):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                SELECT idIncidencia, numNomina_solicitante, fecha_solicitud, 
                    motivo, estatus, aprobado_por_supervisor, aprobado_por_gerente
                FROM incidencias
                WHERE (jefe_directo = ? AND (estatus IN ('Pendiente Supervisor', 'Aprobada', 'Rechazada')))
                OR (gerente_responsable = ? AND (estatus IN ('Pendiente Gerente', 'Aprobada', 'Rechazada')))
                ORDER BY 
                    CASE WHEN estatus IN ('Pendiente Supervisor', 'Pendiente Gerente') THEN 1 ELSE 2 END,
                    idIncidencia {}
            """.format('ASC' if orden == 'asc' else 'DESC')
            
            cursor.execute(query, (numNomina_jefe, numNomina_jefe))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener solicitudes recibidas: {e}")
            return []
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

    def crear_incidencia(self, numNomina_solicitante, nombre_solicitante, apellido_paterno, 
                    apellido_materno, fecha_solicitud, puesto, departamento, 
                    dias_vacaciones, motivo, fecha_inicio, fecha_fin, num_dias, 
                    observaciones, jefe_directo):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Obtener el gerente responsable
            cursor.execute("SELECT jefe_directo FROM usuarios WHERE numNomina = ?", (jefe_directo,))
            gerente_responsable_result = cursor.fetchone()
            gerente_responsable = gerente_responsable_result[0] if gerente_responsable_result else jefe_directo

            # Insertar la incidencia
            cursor.execute("""
                INSERT INTO incidencias (
                    numNomina_solicitante, nombre_solicitante, apellido_paterno, apellido_materno,
                    fecha_solicitud, puesto, departamento, dias_vacaciones, motivo,
                    fecha_inicio, fecha_fin, num_dias, observaciones, jefe_directo, gerente_responsable
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                numNomina_solicitante, nombre_solicitante, apellido_paterno, apellido_materno,
                fecha_solicitud, puesto, departamento, dias_vacaciones, motivo,
                fecha_inicio, fecha_fin, num_dias, observaciones, jefe_directo, gerente_responsable
            ))
            
            conn.commit()
            
            # Notificar al supervisor
            self.enviar_notificacion_incidencia(
                numNomina_solicitante,
                'Nueva solicitud creada',
                motivo,
                fecha_inicio,
                fecha_fin,
                jefe_directo,  # destinatario (supervisor)
                f"Nueva solicitud creada por {nombre_solicitante} {apellido_paterno}"
            )
            
            return True
        except Exception as e:
            print(f"Error al crear incidencia: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_jefe_directo(self, numNomina):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT jefe_directo FROM usuarios
                WHERE numNomina = ?
            """, (numNomina,))
            jefe_directo = cursor.fetchone()
            return jefe_directo[0] if jefe_directo else None
        except Exception as e:
            print(f"Error al obtener jefe directo: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_correo_jefe_directo(self, numNomina):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Obtener el número de nómina del jefe directo
            cursor.execute("""
                SELECT jefe_directo FROM usuarios
                WHERE numNomina = ?
            """, (numNomina,))
            jefe_directo = cursor.fetchone()

            if jefe_directo:
                # Obtener el correo electrónico del jefe directo
                cursor.execute("""
                    SELECT correo_electronico FROM usuarios
                    WHERE numNomina = ?
                """, (jefe_directo[0],))
                correo_jefe = cursor.fetchone()
                return correo_jefe[0] if correo_jefe else None
            return None
        except Exception as e:
            print(f"Error al obtener correo del jefe directo: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def get_incidencia_by_id(self, idIncidencia):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT i.*, 
                    s.nombre as nombre_supervisor, 
                    s.apellidoPaterno as apellido_supervisor,
                    g.nombre as nombre_gerente,
                    g.apellidoPaterno as apellido_gerente
                FROM incidencias i
                LEFT JOIN usuarios s ON i.aprobado_por_supervisor = s.numNomina
                LEFT JOIN usuarios g ON i.aprobado_por_gerente = g.numNomina
                WHERE i.idIncidencia = ?
            """, (idIncidencia,))
            
            incidencia = cursor.fetchone()

            if incidencia:
                # Convertir el resultado en un diccionario para acceder a los campos por nombre
                incidencia_dict = {
                    'idIncidencia': incidencia.idIncidencia,
                    'numNomina_solicitante': incidencia.numNomina_solicitante,
                    'nombre_solicitante': incidencia.nombre_solicitante,
                    'apellido_paterno': incidencia.apellido_paterno,
                    'apellido_materno': incidencia.apellido_materno,
                    'fecha_solicitud': incidencia.fecha_solicitud,
                    'puesto': incidencia.puesto,
                    'departamento': incidencia.departamento,
                    'dias_vacaciones': incidencia.dias_vacaciones,
                    'motivo': incidencia.motivo,
                    'fecha_inicio': incidencia.fecha_inicio,
                    'fecha_fin': incidencia.fecha_fin,
                    'num_dias': incidencia.num_dias,
                    'observaciones': incidencia.observaciones,
                    'estatus': incidencia.estatus,
                    'jefe_directo' : incidencia.jefe_directo,
                    'gerente_responsable' : incidencia.gerente_responsable,
                    'aprobado_por_supervisor' : incidencia.aprobado_por_supervisor,
                    'fecha_aprobacion_supervisor' : incidencia.fecha_aprobacion_supervisor,
                    'aprobado_por_gerente' : incidencia.aprobado_por_gerente,
                    'fecha_aprobacion_gerente' : incidencia.fecha_aprobacion_gerente,
                    'comentarios_supervisor' : incidencia.comentarios_supervisor,
                    'comentarios_gerente' : incidencia.comentarios_gerente
                }
                return incidencia_dict
            return None
        except Exception as e:
            print(f"Error al obtener incidencia por ID: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def actualizar_estatus_incidencia(self, idIncidencia, estatus, numNomina_aprobador, comentarios=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Si es rechazo, marcamos directamente como Rechazada
            if estatus == 'Rechazada':
                cursor.execute("""
                    UPDATE incidencias 
                    SET estatus = 'Rechazada',
                        aprobado_por_supervisor = ?,
                        fecha_aprobacion_supervisor = GETDATE(),
                        comentarios_supervisor = ?
                    WHERE idIncidencia = ?
                """, (numNomina_aprobador, comentarios, idIncidencia))
            else:
                # Lógica normal para otros estados
                current_status = self.get_estatus_incidencia(idIncidencia)
                
                if current_status == 'Pendiente Supervisor':
                    cursor.execute("""
                        UPDATE incidencias 
                        SET estatus = ?,
                            aprobado_por_supervisor = ?,
                            fecha_aprobacion_supervisor = GETDATE(),
                            comentarios_supervisor = ?
                        WHERE idIncidencia = ?
                    """, (estatus, numNomina_aprobador, comentarios, idIncidencia))
                elif current_status == 'Pendiente Gerente':
                    cursor.execute("""
                        UPDATE incidencias 
                        SET estatus = ?,
                            aprobado_por_gerente = ?,
                            fecha_aprobacion_gerente = GETDATE(),
                            comentarios_gerente = ?
                        WHERE idIncidencia = ?
                    """, (estatus, numNomina_aprobador, comentarios, idIncidencia))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar estatus de la incidencia: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def enviar_notificacion_incidencia(self, numNomina, estado, motivo, fecha_inicio, fecha_fin, destinatario=None, aprobador_rol=None):
        """Envía notificación por correo con asunto dinámico"""
        try:
            # Obtener información del solicitante
            solicitante = self.get_user_by_numNomina(numNomina)
            nombre_solicitante = f"{solicitante['nombre']} {solicitante['apellidoPaterno']}" if solicitante else "El usuario"

            # Determinar el asunto según el estado y el rol del aprobador
            if estado.lower() == 'aprobada':
                if aprobador_rol == 'supervisor':
                    asunto = f"Solicitud aprobada por tu supervisor - Pendiente de gerente"
                elif aprobador_rol == 'gerente':
                    asunto = f"¡Felicidades! Tu solicitud ha sido aprobada por el gerente"
                else:
                    asunto = f"Tu solicitud ha sido aprobada"
            elif estado.lower() == 'rechazada':
                if aprobador_rol == 'supervisor':
                    asunto = f"Solicitud rechazada por tu supervisor"
                elif aprobador_rol == 'gerente':
                    asunto = f"Solicitud rechazada por el gerente"
                else:
                    asunto = f"Tu solicitud ha sido rechazada"
            else:
                asunto = f"Actualización en tu solicitud: {estado}"

            # Determinar el destinatario
            if destinatario is None:
                # Notificar al usuario solicitante
                correo_destino = self.get_correo_usuario(numNomina)
                saludo = f"Hola {nombre_solicitante},"
            else:
                # Notificar a supervisor/gerente
                correo_destino = self.get_correo_usuario(destinatario)
                aprobador = self.get_user_by_numNomina(destinatario)
                nombre_aprobador = f"{aprobador['nombre']} {aprobador['apellidoPaterno']}" if aprobador else ""
                saludo = f"Hola {nombre_aprobador}," if nombre_aprobador else "Hola,"

            # Verificar que tenemos un correo destino
            if not correo_destino:
                print(f"No se puede enviar notificación: no hay correo registrado")
                return False

            # Crear el cuerpo del mensaje
            cuerpo = f"""
            <html>
            <body>
                <p>{saludo}</p>
                <h3>{asunto}</h3>
                <p><strong>Detalles de la solicitud:</strong></p>
                <ul>
                    <li><strong>Motivo:</strong> {motivo}</li>
                    <li><strong>Fecha de inicio:</strong> {fecha_inicio}</li>
                    <li><strong>Fecha de fin:</strong> {fecha_fin}</li>
                </ul>
                <br>
                <p>Por favor inicia sesión en el sistema para más detalles.</p>
                <p>Este es un mensaje automático, no responda a este correo.</p>
            </body>
            </html>
            """

            # Configurar y enviar el mensaje
            mensaje = MIMEText(cuerpo, 'html')
            mensaje['Subject'] = asunto
            mensaje['From'] = current_app.config["MAIL_USERNAME"]
            mensaje['To'] = correo_destino

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
            
            print(f"Notificación enviada a {correo_destino}: {asunto}")
            return True
            
        except Exception as e:
            print(f"Error al enviar notificación de incidencia: {e}")
            return False

    def enviar_notificacion_gerente(self, incidencia_id, gerente_nomina, solicitante_nombre, 
                              supervisor_nombre, motivo, fecha_inicio, fecha_fin, comentarios):
        try:
            # Obtener correo del gerente
            correo_gerente = self.get_correo_usuario(gerente_nomina)
            if not correo_gerente:
                print(f"No se encontró correo para el gerente {gerente_nomina}")
                return False

            # Crear enlace directo a la incidencia (ajusta tu URL base)
            enlace_incidencia = f"http://tudominio.com/ver_incidencia/{incidencia_id}/gerente"
            
            # Construir el mensaje
            asunto = f"[URGENTE] Solicitud pendiente de aprobación: {solicitante_nombre}"
            
            cuerpo = f"""
            <html>
            <body>
                <h2>Solicitud pendiente de tu aprobación</h2>
                <p><strong>Solicitante:</strong> {solicitante_nombre}</p>
                <p><strong>Aprobado por supervisor:</strong> {supervisor_nombre}</p>
                <p><strong>Motivo:</strong> {motivo}</p>
                <p><strong>Periodo solicitado:</strong> {fecha_inicio} al {fecha_fin}</p>
                <p><strong>Comentarios del supervisor:</strong> {comentarios or 'Ninguno'}</p>
                <hr>
                <p>Por favor revisa esta solicitud lo antes posible:</p>
                <a href="{enlace_incidencia}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">
                    Revisar Solicitud
                </a>
                <hr>
                <p><small>Este es un mensaje automático. Favor de no responder directamente.</small></p>
            </body>
            </html>
            """

            mensaje = MIMEText(cuerpo, 'html')
            mensaje['Subject'] = asunto
            mensaje['From'] = current_app.config["MAIL_USERNAME"]
            mensaje['To'] = correo_gerente

            # Enviar el correo
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
            print(f"Error al enviar notificación al gerente: {str(e)}")
            return False
        
    def obtener_nombre_usuario(self, numNomina):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT nombre, apellidoPaterno 
                FROM usuarios 
                WHERE numNomina = ?
            """, (numNomina,))
            usuario = cursor.fetchone()
            return f"{usuario[0]} {usuario[1]}" if usuario else f"Nómina {numNomina}"
        except Exception as e:
            print(f"Error al obtener nombre de usuario: {e}")
            return f"Nómina {numNomina}"
        finally:
            cursor.close()
            conn.close()
    
    def get_nombre_usuario(self, numNomina):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT nombre + ' ' + ISNULL(apellidoPaterno, '') 
                FROM usuarios 
                WHERE numNomina = ?
            """, (numNomina,))
            nombre = cursor.fetchone()
            return nombre[0] if nombre else f"Usuario {numNomina}"
        except Exception as e:
            print(f"Error al obtener nombre de usuario: {e}")
            return f"Usuario {numNomina}"
        finally:
            cursor.close()
            conn.close()
    
    def get_correo_usuario(self, numNomina):
        """Obtiene el correo electrónico de un usuario por su número de nómina"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT correo_electronico 
                FROM usuarios 
                WHERE numNomina = ?
            """, (numNomina,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            print(f"Error al obtener correo del usuario: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def get_estatus_incidencia(self, idIncidencia):
        """Obtiene el estado actual de una incidencia"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT estatus FROM incidencias WHERE idIncidencia = ?", (idIncidencia,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            print(f"Error al obtener estado de incidencia: {e}")
            return None
        finally:
            cursor.close()
            conn.close()