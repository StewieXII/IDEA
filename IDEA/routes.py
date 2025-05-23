from flask import render_template, redirect, url_for, flash, request
from . import app, db
from .models import Usuario, Producto, CarritoProducto
from .forms import RegistroForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def home():
    productos = Producto.query.all()
    return render_template('home.html', productos=productos)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistroForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.contraseña.data)
        nuevo_usuario = Usuario(email=form.email.data, contraseña=hashed_pw)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario registrado correctamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and check_password_hash(usuario.contraseña, form.contraseña.data):
            login_user(usuario)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('home'))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

@app.route('/mesas')
def mesas():
    productos = Producto.query.filter(Producto.nombre.ilike('%mesa%')).all()
    return render_template('mesas.html', productos=productos)

@app.route('/sillas')
def sillas():
    productos = Producto.query.filter(Producto.nombre.ilike('%silla%')).all()
    return render_template('sillas.html', productos=productos)

@app.route('/accesorios')
def accesorios():
    productos = Producto.query.filter(Producto.nombre.ilike('%accesorio%')).all()
    return render_template('accesorios.html', productos=productos)

@app.route('/carrito')
@login_required
def carrito():
    items = CarritoProducto.query.filter_by(usuario_id=current_user.id).all()
    return render_template('carrito.html', items=items)

@app.route('/add_to_cart/<int:producto_id>', methods=['POST'])
@login_required
def add_to_cart(producto_id):
    item = CarritoProducto.query.filter_by(usuario_id=current_user.id, producto_id=producto_id).first()
    if item:
        item.cantidad += 1
    else:
        nuevo_item = CarritoProducto(usuario_id=current_user.id, producto_id=producto_id, cantidad=1)
        db.session.add(nuevo_item)
    db.session.commit()
    flash('Producto añadido al carrito.', 'success')
    return redirect(request.referrer or url_for('home'))

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    item = CarritoProducto.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Producto eliminado del carrito.', 'info')
    return redirect(url_for('carrito'))
