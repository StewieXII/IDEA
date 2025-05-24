from flask import render_template, redirect, url_for, flash, request
from . import app, db
from .models import Usuario, Producto, CarritoProducto, Pedido, PedidoProducto
from .forms import RegistroForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from .forms import CheckoutForm

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
        # ... lógica de guardado ...
        flash('Usuario registrado correctamente', 'success')
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
    productos = Producto.query.filter(Producto.categoria == 'mesas').all()
    return render_template('mesas.html', productos=productos)

@app.route('/sillas')
def sillas():
    productos = Producto.query.filter(Producto.categoria == 'sillas').all()
    return render_template('sillas.html', productos=productos)

@app.route('/accesorios')
def accesorios():
    productos = Producto.query.filter(Producto.categoria == 'accesorios').all()
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

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()
    items = CarritoProducto.query.filter_by(usuario_id=current_user.id).all()
    total = sum(item.cantidad * item.producto.precio for item in items)
    if form.validate_on_submit():
        # Crear pedido
        pedido = Pedido(
            usuario_id=current_user.id,
            nombre=form.nombre.data,
            direccion_envio=form.direccion_envio.data,
            metodo_pago=form.metodo_pago.data,
            total=total
        )
        db.session.add(pedido)
        db.session.commit()

        for item in items:
            pedido_prod = PedidoProducto(
                pedido_id=pedido.id,
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio
            )
            db.session.add(pedido_prod)

        # Vaciar carrito
        CarritoProducto.query.filter_by(usuario_id=current_user.id).delete()
        db.session.commit()

        flash("Compra realizada correctamente. ¡Gracias por tu pedido!", "success")
        return redirect(url_for('pedido_confirmacion', pedido_id=pedido.id))

    return render_template('checkout.html', form=form, items=items, total=total)

@app.route('/pedidos')
@login_required
def pedidos():
    pedidos = Pedido.query.filter_by(usuario_id=current_user.id).order_by(Pedido.fecha.desc()).all()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/pedido_confirmacion/<int:pedido_id>')
@login_required
def pedido_confirmacion(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    return render_template('pedido_confirmacion.html', pedido=pedido)

