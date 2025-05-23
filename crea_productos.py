from IDEA import db
from IDEA.models import Producto

# Ejemplo de productos de SILLAS
silla1 = Producto(nombre="Silla Ergonómica", descripcion="Silla ergonómica con respaldo ajustable", imagen="silla-ergonomica.jpg", precio=129.99)
silla2 = Producto(nombre="Silla de Director", descripcion="Silla de director tapizada", imagen="silla-director.jpg", precio=159.99)
silla3 = Producto(nombre="Silla de Visitante", descripcion="Silla de visita, ligera y apilable", imagen="silla-visitante.jpg", precio=79.99)

# Ejemplo de productos de ACCESORIOS
acc1 = Producto(nombre="Organizador de Escritorio", descripcion="Organizador con compartimentos", imagen="organizador-escritorio.jpg", precio=19.99)
acc2 = Producto(nombre="Lámpara LED", descripcion="Lámpara de escritorio con luz LED", imagen="lampara-led.jpg", precio=24.99)
acc3 = Producto(nombre="Soporte para Monitor", descripcion="Soporte ajustable para monitor", imagen="soporte-monitor.jpg", precio=34.99)

db.session.add_all([silla1, silla2, silla3, acc1, acc2, acc3])
db.session.commit()
