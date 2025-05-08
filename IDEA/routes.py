from flask import render_template, redirect, url_for, flash, request
from . import app, db
from .models import Usuario
from .forms import RegistroForm, LoginForm
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

# Cargar usuario desde la base de datos usando su ID
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Página de inicio
@app.route('/')
def home():
    return render_template('home.html')

# Ruta de registro de usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistroForm()  # Suponiendo que RegistroForm tiene solo email y contraseña
    if form.validate_on_submit():
        # Hash de la contraseña
        hashed_pw = generate_password_hash(form.contraseña.data)
        
        # Crear nuevo usuario (sin nombre_usuario, solo email y contraseña)
        nuevo_usuario = Usuario(
            email=form.email.data,
            contraseña=hashed_pw
        )
        
        # Añadir usuario a la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Usuario registrado correctamente. Ahora puedes iniciar sesión.', 'success')
        
        # Redirigir al login después de registrar el usuario
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

# Ruta de login de usuario
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Suponiendo que LoginForm tiene solo email y contraseña
    if form.validate_on_submit():
        # Buscar el usuario en la base de datos por su email
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        
        if usuario and check_password_hash(usuario.contraseña, form.contraseña.data):
            # Iniciar sesión
            login_user(usuario)
            flash('Inicio de sesión exitoso', 'success')

            # Redirigir al home después de iniciar sesión
            return redirect(url_for('home'))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html', form=form)

# Ruta de logout (cerrar sesión)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

# Ruta de mesas (solo ejemplo)
@app.route('/mesas')
def mesas():
    return render_template('mesas.html')

# Ruta de sillas (solo ejemplo)
@app.route('/sillas')
def sillas():
    return render_template('sillas.html')

# Ruta de accesorios (solo ejemplo)
@app.route('/accesorios')
def accesorios():
    return render_template('accesorios.html')

# Ruta de carrito (requiere estar logueado)
@app.route('/carrito')
@login_required
def carrito():
    return render_template('carrito.html')
