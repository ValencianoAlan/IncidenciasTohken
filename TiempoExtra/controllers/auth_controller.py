from flask import Blueprint, render_template, request, redirect, url_for, flash, session

# ⚠️ IMPORTANTE: Asegúrate de que las rutas de importación coincidan con la estructura de tu proyecto.
# Si tu conexión está en otro archivo (ej. database.py), cambia la siguiente línea:
from models.documento import get_db_connection, contar_documentos_pendientes_por_jefe

# Definición del Blueprint para las rutas de Autenticación
auth_bp = Blueprint('auth', __name__)

# ==========================================
# 1. RUTA RAÍZ (REDIRECCIÓN AUTOMÁTICA)
# ==========================================
@auth_bp.route('/')
def index():
    """Redirige al menú si ya hay sesión, o al login si no la hay."""
    if 'usuario_id' in session:
        return redirect(url_for('auth.menu'))
    return redirect(url_for('auth.login'))


# ==========================================
# 2. RUTA DE INICIO DE SESIÓN (GET Y POST)
# ==========================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Maneja la vista del formulario y el procesamiento de credenciales."""
    
    # Si el usuario ya está logueado y trata de entrar a /login, lo mandamos al menú
    if 'usuario_id' in session:
        return redirect(url_for('auth.menu'))
        
    if request.method == 'POST':
        # Obtenemos los datos y quitamos espacios en blanco
        num_nomina = request.form.get('num_nomina').strip()
        password = request.form.get('password').strip()
        
        conn = get_db_connection()
        if not conn:
            flash('❌ Error de conexión a la base de datos.', 'danger')
            return redirect(url_for('auth.login'))
            
        try:
            cursor = conn.cursor()
            
            # Buscamos al usuario y traemos su rol mediante INNER JOIN
            cursor.execute("""
                SELECT u.id, u.num_nomina, u.nombre, ISNULL(u.apellido_paterno, '') AS apellido_paterno, 
                       u.password, r.nombre_rol 
                FROM Usuarios u
                INNER JOIN Roles r ON u.id_rol = r.id_rol
                WHERE u.num_nomina = ?
            """, (num_nomina,))
            
            usuario = cursor.fetchone()
            
            # Validación de credenciales
            if usuario and usuario.password == password:
                
                # 🌟 SE ACTIVA EL TEMPORIZADOR DE INACTIVIDAD (Ej. 15 min configurados en app.py)
                session.permanent = True 
                
                # Guardamos los datos clave en las cookies
                session['usuario_id'] = usuario.id
                session['num_nomina'] = usuario.num_nomina
                session['nombre_usuario'] = usuario.nombre
                session['apellido_usuario'] = usuario.apellido_paterno
                session['rol'] = usuario.nombre_rol
                return redirect(url_for('auth.menu'))
                
            else:
                flash('❌ No. Nómina/ID o contraseña incorrectos.', 'danger')
                return redirect(url_for('auth.login'))
                
        except Exception as e:
            print(f"Error en el login: {e}")
            flash('⚠️ Ocurrió un error interno al intentar iniciar sesión.', 'danger')
            return redirect(url_for('auth.login'))
            
        finally:
            if conn:
                conn.close()
                
    # Si el método es GET (cuando el usuario apenas entra a la página), renderizamos el HTML
    return render_template('login.html')


# ==========================================
# 3. RUTA DEL MENÚ PRINCIPAL
# ==========================================
@auth_bp.route('/menu')
def menu():
    """Carga el menú principal tipo Hub & Spoke con los módulos permitidos."""
    # Validación estricta de seguridad
    if 'usuario_id' not in session:
        flash('🔒 Por favor, inicia sesión para acceder al sistema.', 'warning')
        return redirect(url_for('auth.login'))
        
    rol_actual = session.get('rol')
    nomina_actual = session.get('num_nomina')
    
    # Cálculo de alertas rojas para el panel de revisión (Solo roles de Jefatura)
    alertas_jefe = 0
    if rol_actual in ['Admin', 'Gerente', 'Supervisor', 'Asistente de Gerente', 'Jefe Japonés']:
        alertas_jefe = contar_documentos_pendientes_por_jefe(rol_actual, nomina_actual)
        
    # Enviamos la variable total_pendientes a la vista
    return render_template('menu.html', total_pendientes=alertas_jefe)


# ==========================================
# 4. RUTA DE CIERRE DE SESIÓN
# ==========================================
@auth_bp.route('/logout')
def logout():
    """Destruye la sesión actual y devuelve al usuario a la pantalla de acceso."""
    session.clear() # 🌟 Borra absolutamente todas las variables y cookies del usuario
    flash('🔒 Has cerrado sesión exitosamente. ¡Hasta pronto!', 'info')
    return redirect(url_for('auth.login'))