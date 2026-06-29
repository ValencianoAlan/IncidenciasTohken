from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.usuario import verificar_credenciales

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        num_nomina = request.form.get('num_nomina')
        password = request.form.get('password')
        
        # Consultamos al modelo
        usuario = verificar_credenciales(num_nomina, password)
        
        if usuario:
            # Creamos la sesión en el navegador del usuario
            session['usuario_id'] = usuario.id
            session['num_nomina'] = usuario.num_nomina
            session['nombre_usuario'] = usuario.nombre
            session['rol'] = usuario.rol
            
            flash(f'¡Bienvenido de nuevo, {usuario.nombre}!', 'success')
            return redirect(url_for('auth.menu'))
        else:
            flash('Número de nómina o contraseña incorrectos.', 'danger')
            return redirect(url_for('auth.login'))
            
    return render_template('login.html')


@auth_bp.route('/menu', methods=['GET'])
def menu():
    # Seguridad: Si no ha iniciado sesión, lo regresamos al login
    if 'usuario_id' not in session:
        flash('Por favor, inicia sesión para acceder al menú.', 'danger')
        return redirect(url_for('auth.login'))
        
    return render_template('menu.html')


@auth_bp.route('/logout')
def logout():
    # Limpiamos toda la sesión del navegador
    session.clear()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('auth.login'))