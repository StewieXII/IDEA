# en un archivo crea_productos.py
from IDEA import app, db
from IDEA.models import Producto

with app.app_context():
    p1 = Producto(nombre="Mesa de Oficina", descripcion="Mesa robusta", precio=150.0, categoria="mesa", imagen="img/mesa1.jpg")
    p2 = Producto(nombre="Silla Ergonómica", descripcion="Silla cómoda", precio=75.0, categoria="silla", imagen="img/silla1.jpg")
    p3 = Producto(nombre="Soporte Monitor", descripcion="Soporte ajustable", precio=35.0, categoria="accesorio", imagen="img/accesorio1.jpg")
    db.session.add_all([p1, p2, p3])
    db.session.commit()
