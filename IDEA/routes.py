from flask import render_template
from app import app
from flask import redirect, url_for, flash, request
from app.forms import LoginForm, RegisterForm
from app.models import Usuario
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/mesas')
def mesas():
    return render_template('mesas.html')

@app.route('/sillas')
def sillas():
    return render_template('sillas.html')

@app.route('/accesorios')
def accesorios():
    return render_template('accesorios.html')

@app.route('/carrito')
def carrito():
    
    return render_template('carrito.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            return redirect(url_for('home'))
        else:
            flash('Email o contraseña incorrectos')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        nuevo_usuario = Usuario(nombre=form.nombre.data, email=form.email.data, password=hashed_pw)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
